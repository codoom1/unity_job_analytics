"""
app.py
------
This module provides the main entry point for the dashboard web application.
It typically sets up the web server, routes, and integrates analytics modules for reporting and visualization.

Update this docstring as you add or modify functions/classes in this file.
"""

import streamlit as st
import pandas as pd
import duckdb
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import seaborn as sns
import sys
import os

import sys
import os

# Add parent directory to Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analytics.gpu_metrics import GPUMetrics, vram_cutoffs, vram_labels
from outreach.email_templates import generate_email, generate_comprehensive_email

st.set_page_config(layout="wide")
st.title("Unity GPU Job Analytics Dashboard")

# Initialize GPU Metrics
import pathlib

@st.cache_resource
def load_metrics():
    try:
        # Always resolve path relative to project root
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        db_path = os.path.join(project_root, "data/raw/slurm_data_small.db")
        return GPUMetrics(metricsfile=db_path, min_elapsed=600)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

metrics = load_metrics()

if metrics is None or metrics.df.empty:
    st.error("Could not load GPU metrics data. Please check the database connection.")
else:
    data = metrics.df
    
    # Sidebar filters
    st.sidebar.header("Filters")
    days_back = st.sidebar.slider("Days to analyze", 1, 365, 60)
    cutoff = datetime.now() - timedelta(days=days_back)

    # Get unique PI groups and users
    pi_groups = sorted(data['Account'].unique())
    selected_pi = st.sidebar.selectbox("Select PI Group", ["All"] + list(pi_groups))

    try:
        # Filter data by date with fallback
        filtered_data = data[data['StartTime'] >= cutoff]
        if filtered_data.empty:
            st.warning(f"No data found in last {days_back} days, using all available data")
            filtered_data = data
        
        # Main dashboard
        col1, col2 = st.columns(2)

        with col1:
            st.write("## GPU Usage Summary")
            if selected_pi != "All":
                metrics.pi_report(selected_pi, days_back=days_back, vram=True, aggregate=True)
            
            st.write("### GPU Type Distribution")
            fig, ax = plt.subplots()
            filtered_data['GPUType'].explode().value_counts().plot(kind='bar')
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with col2:
            st.write("## Memory Usage Analysis")
            fig, ax = plt.subplots(figsize=(10, 6))
            # Use filtered data constraints
            constrs = [] if selected_pi == "All" else [f"Account='{selected_pi}'"]
            if not filtered_data.equals(data):  # Only add date filter if we have recent data
                constrs.append(f"StartTime>='{cutoff}'")
            
            metrics.efficiency_plot(
                constrs=constrs,
                title="GPU VRAM Usage Distribution"
            )
            st.pyplot(fig)

        # Wait time analysis
        st.write("## Queue Wait Times")
        metrics.waittime(days_back=days_back)

        # Underutilization analysis
        st.write("## Underutilized Jobs")
        threshold = st.slider("Memory Usage Threshold (%)", 0, 100, 10)
        underutilized = filtered_data[
            (filtered_data['GPUMemUsage'] < threshold/100 * filtered_data['GPUs'] * 80 * 2**30)
        ]
        if selected_pi != "All":
            underutilized = underutilized[underutilized['Account'] == selected_pi]

        st.dataframe(
            underutilized[['JobID', 'User', 'Account', 'GPUMemUsage', 'GPUs', 'StartTime']]
            .sort_values('StartTime', ascending=False)
        )
        
        # Email Outreach Section
        st.write("## 📧 Email Outreach for Underutilized Jobs")
        
        if not underutilized.empty:
            # Calculate user-level statistics for outreach
            user_stats = underutilized.groupby('User').agg({
                'JobID': 'count',
                'GPUMemUsage': 'sum',
                'StartTime': 'max',
                'Account': 'first'
            }).rename(columns={
                'JobID': 'WastedJobs',
                'GPUMemUsage': 'TotalWastedGB',
                'StartTime': 'LastJob',
                'Account': 'PI'
            })
            user_stats['TotalWastedGB'] = user_stats['TotalWastedGB'] / (2**30)  # Convert to GB
            
            # Filter for significant waste (similar to zero_gpu_usage_list.py criteria)
            min_wasted_jobs = st.number_input("Minimum wasted jobs for outreach", min_value=1, value=3)
            min_wasted_gb = st.number_input("Minimum wasted GPU memory (GB) for outreach", min_value=1.0, value=4.0)
            
            flagged_users = user_stats[
                (user_stats['WastedJobs'] >= min_wasted_jobs) & 
                (user_stats['TotalWastedGB'] >= min_wasted_gb)
            ].sort_values('TotalWastedGB', ascending=False)
            
            if not flagged_users.empty:
                st.write(f"### 🚨 {len(flagged_users)} Users Flagged for Outreach")
                st.dataframe(flagged_users)
                
                # Email preview section
                selected_user = st.selectbox(
                    "Select user to preview email:", 
                    ["None"] + list(flagged_users.index)
                )
                
                if selected_user != "None":
                    st.write(f"### 📧 Email Preview for {selected_user}")
                    
                    # Get sample jobs for this user
                    user_jobs = underutilized[underutilized['User'] == selected_user].head(5)
                    job_samples = []
                    interactive_count = 0
                    
                    for _, job in user_jobs.iterrows():
                        job_samples.append({
                            'JobID': job['JobID'],
                            'GPUMemUsage': job['GPUMemUsage']
                        })
                        if job.get('Interactive', False):
                            interactive_count += 1
                    
                    # Prepare user data for comprehensive email
                    user_data = flagged_users.loc[selected_user].to_dict()
                    user_data['Interactive'] = interactive_count
                    
                    # Email template selection
                    email_style = st.radio(
                        "Email Style:",
                        ["Simple", "Comprehensive (matching zero_gpu_usage_list.py)"],
                        index=1
                    )
                    
                    if email_style == "Simple":
                        email_content = generate_email(selected_user, job_samples)
                    else:
                        email_content = generate_comprehensive_email(selected_user, user_data, job_samples)
                    
                    st.text_area("Email Content:", email_content, height=400)
                    
                    # Show job details for context
                    st.write("#### Recent Underutilized Jobs:")
                    st.dataframe(
                        user_jobs[['JobID', 'StartTime', 'GPUMemUsage', 'GPUs']]
                        .assign(GPUMemUsage_GB=lambda x: x['GPUMemUsage'] / (2**30))
                        .drop('GPUMemUsage', axis=1)
                        .rename(columns={'GPUMemUsage_GB': 'GPU Memory Used (GB)'})
                    )
                    
                    # Action buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📋 Copy Email to Clipboard"):
                            st.code(email_content, language="text")
                            st.success("Email content displayed above - you can copy it manually")
                    
                    with col2:
                        if st.button("📊 Generate Report for All Flagged Users"):
                            st.write("### 📊 Outreach Report")
                            for user in flagged_users.index:
                                user_jobs = underutilized[underutilized['User'] == user].head(5)
                                job_samples = []
                                interactive_count = 0
                                
                                for _, job in user_jobs.iterrows():
                                    job_samples.append({
                                        'JobID': job['JobID'],
                                        'GPUMemUsage': job['GPUMemUsage']
                                    })
                                    if job.get('Interactive', False):
                                        interactive_count += 1
                                
                                user_data = flagged_users.loc[user].to_dict()
                                user_data['Interactive'] = interactive_count
                                
                                st.write(f"**User: {user}**")
                                st.write(f"- Wasted Jobs: {flagged_users.loc[user, 'WastedJobs']}")
                                st.write(f"- Total Wasted GPU Memory: {flagged_users.loc[user, 'TotalWastedGB']:.1f} GB")
                                st.write(f"- PI Group: {flagged_users.loc[user, 'PI']}")
                                st.write(f"- Last Job: {flagged_users.loc[user, 'LastJob']}")
                                st.write(f"- Interactive Jobs: {interactive_count}/{flagged_users.loc[user, 'WastedJobs']}")
                                
                                with st.expander(f"📧 Email for {user}"):
                                    email_content = generate_comprehensive_email(user, user_data, job_samples)
                                    st.text(email_content)
                                    
                                    st.write("**Recent Underutilized Jobs:**")
                                    st.dataframe(
                                        user_jobs[['JobID', 'StartTime', 'GPUMemUsage', 'GPUs']]
                                        .assign(GPUMemUsage_GB=lambda x: x['GPUMemUsage'] / (2**30))
                                        .drop('GPUMemUsage', axis=1)
                                        .rename(columns={'GPUMemUsage_GB': 'GPU Memory Used (GB)'})
                                    )
                                st.write("---")
            else:
                st.info("No users meet the criteria for outreach based on current thresholds.")
        else:
            st.info("No underutilized jobs found with current filters.")
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
