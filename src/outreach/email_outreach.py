#!/usr/bin/env python3
"""
Email Outreach Tool for Underutilized GPU Jobs

This tool identifies users with underutilized GPU jobs and generates personalized
outreach emails similar to zero_gpu_usage_list.py but with enhanced functionality.
"""

"""
email_outreach.py
----------------
This module provides functions and/or classes for sending outreach emails to users or groups.
It may include logic for composing, sending, and tracking email communications.

Update this docstring as you add or modify functions/classes in this file.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import duckdb
import pandas as pd
from fire import Fire
from datetime import datetime, timedelta
from analytics.gpu_metrics import GPUMetrics
from outreach.email_templates import generate_comprehensive_email, INTRO, HOURS, get_job_type_breakdown

def main(dbfile="../../data/raw/slurm_data_small.db", 
         days_back=60, 
         min_wasted_jobs=3, 
         min_wasted_gb=4.0,
         memory_threshold=10,
         email=False,
         userlist="users.csv"):
    """
    Generate outreach emails for users with underutilized GPU jobs.
    
    Args:
        dbfile: Path to DuckDB database file
        days_back: Number of days to look back for job data
        min_wasted_jobs: Minimum number of wasted jobs to trigger outreach
        min_wasted_gb: Minimum GB of wasted GPU memory to trigger outreach
        memory_threshold: Memory usage threshold percentage (jobs below this are considered wasted)
        email: If True, generate and display emails; if False, just show summary
        userlist: Path to CSV file with user information (username, email, first_name)
    """
    
    print(f"🔍 Analyzing GPU job data from last {days_back} days...")
    print(f"📊 Criteria: ≥{min_wasted_jobs} jobs, ≥{min_wasted_gb} GB wasted, <{memory_threshold}% memory usage")
    print("=" * 80)
    
    # Load GPU metrics
    try:
        metrics = GPUMetrics(metricsfile=dbfile)
        print(f"✅ Loaded {len(metrics.df)} GPU jobs from database")
    except Exception as e:
        print(f"❌ Error loading database: {e}")
        return
    
    df = metrics.df
    cutoff = datetime.now() - timedelta(days=days_back)
    
    # Filter data with fallback logic (matching our dashboard approach)
    try:
        filtered_df = df[df['StartTime'] >= cutoff]
        if filtered_df.empty:
            print(f"⚠️  No data found in last {days_back} days, using all available data...")
            filtered_df = df
        else:
            print(f"📅 Using {len(filtered_df)} jobs from last {days_back} days")
    except Exception as e:
        print(f"⚠️  Date filtering failed, using all data: {e}")
        filtered_df = df
    
    # Calculate memory threshold (assuming 80GB per GPU as typical)
    gpu_memory_per_gpu = 80 * (2**30)  # 80 GB in bytes
    threshold_bytes = (memory_threshold / 100) * gpu_memory_per_gpu
    
    # Identify underutilized jobs
    underutilized = filtered_df[
        filtered_df['GPUMemUsage'] < threshold_bytes * filtered_df['GPUs']
    ]
    
    if underutilized.empty:
        print("✅ No underutilized jobs found with current criteria!")
        return
    
    print(f"🎯 Found {len(underutilized)} underutilized jobs")
    
    # Group by user and calculate statistics
    user_stats = underutilized.groupby('User').agg({
        'JobID': 'count',
        'GPUMemUsage': 'sum', 
        'StartTime': 'max',
        'Account': 'first',
        'Interactive': lambda x: x.notna().sum()  # Count interactive jobs
    }).rename(columns={
        'JobID': 'WastedJobs',
        'GPUMemUsage': 'TotalWastedBytes',
        'StartTime': 'LastJob',
        'Account': 'PI'
    })
    
    # Convert to GB and calculate additional metrics
    user_stats['TotalWastedGB'] = user_stats['TotalWastedBytes'] / (2**30)
    user_stats['WastedGPUHours'] = user_stats['TotalWastedGB'] / 80  # Approximate GPU hours
    
    # Filter users meeting outreach criteria
    flagged_users = user_stats[
        (user_stats['WastedJobs'] >= min_wasted_jobs) & 
        (user_stats['TotalWastedGB'] >= min_wasted_gb)
    ].sort_values('TotalWastedGB', ascending=False)
    
    if flagged_users.empty:
        print("✅ No users meet the outreach criteria!")
        print("\n📊 Summary of underutilization:")
        summary = user_stats.describe()[['WastedJobs', 'TotalWastedGB']]
        print(summary.round(2).to_string())
        return
    
    print(f"🚨 {len(flagged_users)} users flagged for outreach:")
    print()
    
    # Display summary table
    display_cols = ['WastedJobs', 'TotalWastedGB', 'Interactive', 'PI', 'LastJob']
    summary_table = flagged_users[display_cols].copy()
    summary_table.columns = ['Jobs', 'Wasted GB', 'Interactive', 'PI Group', 'Last Job']
    print(summary_table.round(1).to_string())
    print()
    
    # Generate emails if requested
    if email:
        print("📧 GENERATING OUTREACH EMAILS")
        print("=" * 80)
        
        # Try to load user information
        try:
            if userlist and userlist != "users.csv":  # Custom userlist provided
                users = pd.read_csv(userlist).set_index("username")
                print(f"✅ Loaded user information from {userlist}")
            else:
                print(f"⚠️  User list file '{userlist}' not found, using usernames only")
                users = None
        except Exception as e:
            print(f"⚠️  Could not load user list: {e}")
            users = None
        
        for idx, (username, user_data) in enumerate(flagged_users.iterrows(), 1):
            print(f"\n📧 EMAIL {idx}/{len(flagged_users)} - User: {username}")
            print("-" * 60)
            
            # Get sample jobs for this user
            user_jobs = underutilized[underutilized['User'] == username].head(5)
            job_samples = []
            for _, job in user_jobs.iterrows():
                job_samples.append({
                    'JobID': job['JobID'],
                    'GPUMemUsage': job['GPUMemUsage']
                })
            
            # Get user's real name if available
            if users is not None and username in users.index:
                user_info = users.loc[username]
                display_name = user_info.get('first', username)
                user_email = user_info.get('email', f"{username}@university.edu")
                print(f"📬 To: {user_email} ({display_name})")
            else:
                display_name = username
                user_email = f"{username}@university.edu"
                print(f"📬 To: {user_email}")
            
            print(f"📊 Stats: {int(user_data['WastedJobs'])} jobs, {user_data['TotalWastedGB']:.1f} GB wasted")
            
            # Generate email using comprehensive template
            email_content = generate_comprehensive_email(display_name, user_data, job_samples)
            
            print("\n📄 EMAIL CONTENT:")
            print("-" * 40)
            print(email_content)
            
            # Show recent job details
            print("\n📋 RECENT UNDERUTILIZED JOBS:")
            job_details = user_jobs[['JobID', 'StartTime', 'GPUMemUsage', 'GPUs']].copy()
            job_details['GPU_Memory_GB'] = job_details['GPUMemUsage'] / (2**30)
            job_details = job_details[['JobID', 'StartTime', 'GPU_Memory_GB', 'GPUs']]
            print(job_details.round(2).to_string(index=False))
            
            if idx < len(flagged_users):
                print("\n" + "=" * 80)
    else:
        print("💡 Use --email=True to generate actual email content")
        print("💡 Use --userlist=path/to/users.csv to include real names and email addresses")

if __name__ == "__main__":
    Fire(main)
