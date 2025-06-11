# Jupyter Notebooks Guide

The SLURM Job Analytics project includes Jupyter notebooks for interactive data exploration and analysis. This guide covers how to use and extend the notebooks for your research.

## 🎯 Overview

The project includes several Jupyter notebooks:

- **`SlurmGPU.ipynb`**: Main analysis notebook with comprehensive examples
- **`explore.ipynb`**: Data exploration and custom analysis workspace

These notebooks provide interactive environments for:
- Exploratory data analysis
- Custom visualizations
- Advanced statistical analysis
- Prototyping new features

## 🚀 Getting Started

### Setting Up Jupyter

1. **Install Jupyter in your environment**:
   ```bash
   source duckdb/bin/activate
   pip install jupyter ipykernel
   ```

2. **Register the kernel**:
   ```bash
   python -m ipykernel install --user --name "ds4cg-analytics" --display-name "DS4CG Analytics"
   ```

3. **Launch Jupyter**:
   ```bash
   jupyter notebook
   ```

### Opening the Notebooks

Navigate to the notebooks directory and open either:
- `notebooks/SlurmGPU.ipynb` - Main analysis notebook
- `notebooks/explore.ipynb` - Custom exploration workspace

## 📊 Main Analysis Notebook (`SlurmGPU.ipynb`)

### Notebook Structure

The main notebook is organized into several sections:

#### 1. Environment Setup

```python
# Import modules and load the dataframe with job information
import duckdb
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns

# Set plotting style
sns.set_theme()
sns.set_palette("muted")

# Load GPU metrics (jobs > 10 minutes)
from analytics.gpu_metrics import GPUMetrics
metrics = GPUMetrics(min_elapsed=600)
df = metrics.df

print(f"Loaded {len(df)} GPU jobs")
```

#### 2. Basic Data Exploration

```python
# Display basic statistics
print("Dataset Overview:")
print(f"Date range: {df['StartTime'].min()} to {df['StartTime'].max()}")
print(f"Total jobs: {len(df):,}")
print(f"Unique users: {df['User'].nunique():,}")
print(f"Unique PI groups: {df['Account'].nunique():,}")

# Show column information
df.info()
```

#### 3. Queue Time Analysis

**Relationship between time limit and queue time**:

```python
def do_relplot():
    """Plot relationship between timelimit and queue time"""
    mask = (~df["IsArray"] & (df["GPUs"]==1) & (df['Partition']=='gpu')) 
    plotting_df = pd.DataFrame({
        "Queued Hours": df["queued_seconds"][mask]/3600,
        "Requested Hours": df["TimeLimit"][mask]/60,
        "Requested VRAM (G)": df["requested_vram"][mask],
    }).clip(0,100)
    
    sns.relplot(data=plotting_df, x='Requested Hours', y="Queued Hours", 
                hue="Requested VRAM (G)")

do_relplot()
```

**Queue time statistics by GPU type**:

```python
def plot_queued(stat="Median"):
    """Plot queue time statistics by GPU type"""
    df_filtered = df[~df["IsArray"] & (df["GPUs"] == 1)]
    
    # Calculate statistics
    if stat == "Median":
        queue_stats = df_filtered.groupby("requested_vram")["queued_seconds"].median() / 3600
    else:
        queue_stats = df_filtered.groupby("requested_vram")["queued_seconds"].mean() / 3600
    
    # Create plot
    plt.figure(figsize=(10, 6))
    queue_stats.plot(kind='bar')
    plt.title(f'{stat} Queue Time by Requested VRAM')
    plt.xlabel('Requested VRAM (GB)')
    plt.ylabel('Queue Time (hours)')
    plt.xticks(rotation=45)
    plt.tight_layout()

plot_queued(stat="Median")
```

#### 4. Memory Usage Analysis

**VRAM usage distribution**:

```python
def efficiency_plot(constrs=[], title="Used GPU VRAM by GPU Compute Hours"):
    """Create efficiency plot showing VRAM usage vs compute hours"""
    if len(constrs):
        where = "where " + (" and ".join(constrs))
    else:
        where = ""
    
    filtered_df = duckdb.query(
        f"select GPUs, GPUMemUsage, Elapsed, requested_vram, IsArray"
        ", Elapsed*GPUs/3600 as gpu_hours "
        " from df " + where 
    ).df()
    
    # Convert memory to GB
    filtered_df['GPUMemUsage_GB'] = filtered_df['GPUMemUsage'] / (2**30)
    
    # Create scatter plot
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(filtered_df['gpu_hours'], filtered_df['GPUMemUsage_GB'], 
                         c=filtered_df['requested_vram'], alpha=0.6, s=20)
    plt.colorbar(scatter, label='Requested VRAM (GB)')
    plt.xlabel('GPU Compute Hours')
    plt.ylabel('Used GPU Memory (GB)')
    plt.title(title)
    plt.grid(True, alpha=0.3)

# Plot all jobs
efficiency_plot()

# Plot jobs with specific constraints
efficiency_plot(constrs=['requested_vram>=80'], 
                title="Used GPU VRAM by GPU Compute Hours (80GB+ requests)")
```

#### 5. Advanced Analysis Examples

**Memory utilization by user**:

```python
# Analyze memory utilization patterns by user
user_analysis = df.groupby('User').agg({
    'JobID': 'count',
    'GPUMemUsage': 'mean',
    'GPUs': 'sum',
    'Elapsed': 'sum'
}).rename(columns={
    'JobID': 'total_jobs',
    'GPUMemUsage': 'avg_memory_usage',
    'GPUs': 'total_gpus_used',
    'Elapsed': 'total_runtime'
})

# Calculate efficiency metrics
user_analysis['avg_memory_gb'] = user_analysis['avg_memory_usage'] / (2**30)
user_analysis['total_gpu_hours'] = user_analysis['total_runtime'] * user_analysis['total_gpus_used'] / 3600

# Show top users by GPU hours
top_users = user_analysis.sort_values('total_gpu_hours', ascending=False).head(10)
print("Top 10 Users by GPU Hours:")
print(top_users[['total_jobs', 'avg_memory_gb', 'total_gpu_hours']])
```

### Interactive Widgets

The notebook includes interactive widgets for dynamic exploration:

```python
import ipywidgets as widgets
from IPython.display import display

# Interactive date range selector
date_range = widgets.SelectionRangeSlider(
    options=df['StartTime'].dt.date.unique(),
    index=(0, len(df['StartTime'].dt.date.unique())-1),
    description='Date Range',
    disabled=False
)

# Interactive PI group selector
pi_selector = widgets.Dropdown(
    options=['All'] + sorted(df['Account'].unique()),
    value='All',
    description='PI Group:'
)

def update_analysis(date_range, pi_group):
    """Update analysis based on widget selections"""
    filtered_df = df.copy()
    
    # Apply date filter
    if date_range:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['StartTime'].dt.date >= start_date) &
            (filtered_df['StartTime'].dt.date <= end_date)
        ]
    
    # Apply PI group filter
    if pi_group != 'All':
        filtered_df = filtered_df[filtered_df['Account'] == pi_group]
    
    # Display updated statistics
    print(f"Filtered dataset: {len(filtered_df)} jobs")
    print(f"Date range: {filtered_df['StartTime'].min()} to {filtered_df['StartTime'].max()}")
    
    # Create updated visualization
    plt.figure(figsize=(10, 6))
    memory_gb = filtered_df['GPUMemUsage'] / (2**30)
    plt.hist(memory_gb, bins=50, alpha=0.7, edgecolor='black')
    plt.xlabel('GPU Memory Usage (GB)')
    plt.ylabel('Number of Jobs')
    plt.title(f'GPU Memory Usage Distribution - {pi_group}')
    plt.show()

# Create interactive interface
widgets.interact(update_analysis, 
                date_range=date_range, 
                pi_group=pi_selector)
```

## 🔍 Custom Analysis Examples

### Time Series Analysis

```python
# Analyze usage trends over time
daily_usage = df.groupby(df['StartTime'].dt.date).agg({
    'JobID': 'count',
    'GPUs': 'sum',
    'Elapsed': 'sum',
    'GPUMemUsage': 'mean'
}).rename(columns={
    'JobID': 'daily_jobs',
    'GPUs': 'daily_gpus',
    'Elapsed': 'daily_runtime',
    'GPUMemUsage': 'avg_memory'
})

# Calculate daily GPU hours
daily_usage['daily_gpu_hours'] = (daily_usage['daily_runtime'] * daily_usage['daily_gpus']) / 3600

# Plot trends
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

daily_usage['daily_jobs'].plot(ax=axes[0,0], title='Daily Job Count')
daily_usage['daily_gpu_hours'].plot(ax=axes[0,1], title='Daily GPU Hours')
daily_usage['avg_memory'].plot(ax=axes[1,0], title='Average Memory Usage')
(daily_usage['avg_memory'] / (2**30)).plot(ax=axes[1,1], title='Average Memory Usage (GB)')

plt.tight_layout()
plt.show()
```

### Efficiency Analysis

```python
# Calculate various efficiency metrics
df['memory_efficiency'] = df['GPUMemUsage'] / (df['GPUs'] * 80 * (2**30))  # Assuming 80GB GPUs
df['queue_efficiency'] = df['Elapsed'] / (df['Elapsed'] + df['queued_seconds'])

# Efficiency by PI group
efficiency_by_pi = df.groupby('Account').agg({
    'memory_efficiency': ['mean', 'median', 'std'],
    'queue_efficiency': ['mean', 'median', 'std'],
    'JobID': 'count'
}).round(3)

print("Efficiency by PI Group:")
print(efficiency_by_pi.head(10))

# Visualize efficiency distribution
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

df['memory_efficiency'].hist(bins=50, ax=axes[0], alpha=0.7)
axes[0].set_title('Memory Efficiency Distribution')
axes[0].set_xlabel('Memory Efficiency (0-1)')

df['queue_efficiency'].hist(bins=50, ax=axes[1], alpha=0.7)
axes[1].set_title('Queue Efficiency Distribution')
axes[1].set_xlabel('Queue Efficiency (0-1)')

plt.tight_layout()
plt.show()
```

### Machine Learning Analysis

```python
# Predictive modeling for queue times
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

# Prepare features for queue time prediction
features = ['GPUs', 'requested_vram', 'TimeLimit', 'hour_of_day', 'day_of_week']

# Extract time features
df['hour_of_day'] = df['SubmitTime'].dt.hour
df['day_of_week'] = df['SubmitTime'].dt.dayofweek

# Prepare data
X = df[features].fillna(0)
y = df['queued_seconds'] / 3600  # Convert to hours

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate
y_pred = rf_model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Queue Time Prediction Model:")
print(f"Mean Absolute Error: {mae:.2f} hours")
print(f"R² Score: {r2:.3f}")

# Feature importance
feature_importance = pd.DataFrame({
    'feature': features,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nFeature Importance:")
print(feature_importance)
```

## 📝 Creating Custom Notebooks

### Starting a New Analysis

1. **Copy the template**:
   ```bash
   cp notebooks/SlurmGPU.ipynb notebooks/my_analysis.ipynb
   ```

2. **Set up your environment**:
   ```python
   # Standard imports
   import sys
   sys.path.append('../src')
   
   import pandas as pd
   import matplotlib.pyplot as plt
   import seaborn as sns
   from analytics.gpu_metrics import GPUMetrics
   from analytics.cpu_metrics import CPUMetrics
   
   # Configure plotting
   %matplotlib inline
   sns.set_theme()
   plt.rcParams['figure.figsize'] = [12, 8]
   ```

3. **Load and explore your data**:
   ```python
   # Load data with custom filters
   gpu_metrics = GPUMetrics(min_elapsed=1800)  # 30+ minute jobs
   cpu_metrics = CPUMetrics(min_elapsed=1800)
   
   gpu_df = gpu_metrics.df
   cpu_df = cpu_metrics.df
   
   print(f"GPU jobs: {len(gpu_df)}")
   print(f"CPU jobs: {len(cpu_df)}")
   ```

### Best Practices for Notebook Development

#### Organization

```python
# Use clear section headers
# =============================================================================
# 1. DATA LOADING AND PREPROCESSING
# =============================================================================

# =============================================================================
# 2. EXPLORATORY DATA ANALYSIS
# =============================================================================

# =============================================================================
# 3. VISUALIZATION AND ANALYSIS
# =============================================================================
```

#### Documentation

```python
"""
Analysis Notebook: GPU Utilization Patterns

Objective: Analyze GPU utilization patterns across different research groups
to identify optimization opportunities.

Author: Your Name
Date: 2025-06-09
"""

# Document your analysis steps
def analyze_gpu_patterns(df, pi_group=None):
    """
    Analyze GPU utilization patterns for a specific PI group or all groups.
    
    Parameters:
    - df: DataFrame with GPU job data
    - pi_group: Optional PI group filter
    
    Returns:
    - Dictionary with analysis results
    """
    # Implementation here
    pass
```

#### Reproducibility

```python
# Set random seeds for reproducible results
import numpy as np
np.random.seed(42)

# Use relative paths
import os
data_path = os.path.join('..', 'data', 'raw', 'slurm_data_small.db')

# Save intermediate results
results = analyze_gpu_patterns(df)
results_df = pd.DataFrame(results)
results_df.to_csv('../data/processed/gpu_analysis_results.csv', index=False)
```

## 🎨 Advanced Visualizations

### Interactive Plots with Plotly

```python
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Interactive scatter plot
fig = px.scatter(df, 
                 x='Elapsed', 
                 y='GPUMemUsage',
                 color='Account',
                 size='GPUs',
                 hover_data=['User', 'JobID'],
                 title='GPU Memory Usage vs Job Duration')

fig.update_layout(height=600)
fig.show()

# Interactive time series
daily_stats = df.groupby(df['StartTime'].dt.date).agg({
    'JobID': 'count',
    'GPUMemUsage': 'mean'
}).reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(x=daily_stats['StartTime'], 
                        y=daily_stats['JobID'],
                        name='Daily Jobs'))

fig.update_layout(title='Daily Job Submission Trends')
fig.show()
```

### Custom Dashboard Components

```python
# Create a mini-dashboard within the notebook
from ipywidgets import interact, Layout, VBox, HBox
import ipywidgets as widgets

# Control panel
controls = {
    'pi_group': widgets.Dropdown(options=['All'] + sorted(df['Account'].unique()),
                                 description='PI Group:'),
    'min_gpus': widgets.IntSlider(min=1, max=8, value=1, description='Min GPUs:'),
    'time_period': widgets.IntSlider(min=7, max=365, value=30, description='Days:')
}

# Display function
def dashboard_display(**kwargs):
    filtered_df = df.copy()
    
    # Apply filters
    if kwargs['pi_group'] != 'All':
        filtered_df = filtered_df[filtered_df['Account'] == kwargs['pi_group']]
    
    filtered_df = filtered_df[filtered_df['GPUs'] >= kwargs['min_gpus']]
    
    cutoff_date = df['StartTime'].max() - pd.Timedelta(days=kwargs['time_period'])
    filtered_df = filtered_df[filtered_df['StartTime'] >= cutoff_date]
    
    # Create visualizations
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Memory usage histogram
    memory_gb = filtered_df['GPUMemUsage'] / (2**30)
    axes[0].hist(memory_gb, bins=30, alpha=0.7)
    axes[0].set_title('Memory Usage Distribution')
    axes[0].set_xlabel('GPU Memory (GB)')
    
    # Jobs over time
    daily_jobs = filtered_df.groupby(filtered_df['StartTime'].dt.date).size()
    daily_jobs.plot(ax=axes[1])
    axes[1].set_title('Daily Job Count')
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    # Summary statistics
    print(f"Filtered dataset: {len(filtered_df)} jobs")
    print(f"Average memory usage: {memory_gb.mean():.1f} GB")
    print(f"Total GPU hours: {(filtered_df['Elapsed'] * filtered_df['GPUs']).sum() / 3600:.0f}")

# Create interactive dashboard
interact(dashboard_display, **controls)
```

## 💾 Saving and Sharing Results

### Exporting Analysis Results

```python
# Save analysis results
analysis_results = {
    'dataset_size': len(df),
    'date_range': f"{df['StartTime'].min()} to {df['StartTime'].max()}",
    'total_gpu_hours': (df['Elapsed'] * df['GPUs']).sum() / 3600,
    'average_memory_usage_gb': (df['GPUMemUsage'] / (2**30)).mean(),
    'top_pi_groups': df['Account'].value_counts().head(5).to_dict()
}

# Save to JSON
import json
with open('../data/processed/analysis_summary.json', 'w') as f:
    json.dump(analysis_results, f, indent=2, default=str)

# Save key plots
plt.figure(figsize=(12, 8))
# Your plot code here
plt.savefig('../data/processed/gpu_efficiency_analysis.png', dpi=300, bbox_inches='tight')
```

### Creating Reports

```python
# Generate a report markdown file
report_content = f"""
# GPU Utilization Analysis Report

**Analysis Date**: {pd.Timestamp.now().strftime('%Y-%m-%d')}
**Dataset**: {len(df):,} GPU jobs
**Date Range**: {df['StartTime'].min()} to {df['StartTime'].max()}

## Key Findings

- Total GPU hours analyzed: {(df['Elapsed'] * df['GPUs']).sum() / 3600:.0f}
- Average memory utilization: {(df['GPUMemUsage'] / (2**30)).mean():.1f} GB
- Most active PI group: {df['Account'].value_counts().index[0]} ({df['Account'].value_counts().iloc[0]} jobs)

## Recommendations

1. Focus optimization efforts on low-efficiency jobs
2. Provide GPU programming training for underutilizing groups
3. Consider smaller GPU allocations for memory-light workloads

![GPU Efficiency Analysis](gpu_efficiency_analysis.png)
"""

with open('../data/processed/analysis_report.md', 'w') as f:
    f.write(report_content)
```

The Jupyter notebooks provide a powerful platform for interactive analysis and visualization. Use them to explore your data, prototype new analyses, and create compelling visualizations for presentations and reports!
