# Command Line Tools Guide

The SLURM Job Analytics project provides powerful command-line tools for analyzing GPU and CPU job data. This guide covers all available tools and their usage.

## 🎯 Overview

The command-line tools are organized into three main categories:

- **Analytics Tools**: Core analysis functions for GPU and CPU jobs
- **Outreach Tools**: User notification and email generation
- **Utility Scripts**: Data export and maintenance tasks

## 📊 Analytics Tools

### GPU Metrics (`gpu_metrics.py`)

Located in `src/analytics/`, this tool provides comprehensive GPU job analysis.

#### Basic Usage

```bash
cd src/analytics
python gpu_metrics.py [COMMAND] [OPTIONS]
```

#### Available Commands

##### Wait Time Analysis

```bash
# Analyze queue wait times by GPU type
python gpu_metrics.py waittime

# Analyze specific time period
python gpu_metrics.py waittime --days_back=30

# Analyze specific partition
python gpu_metrics.py waittime --partition=gpu
```

**Example Output**:
```
GPU Wait Time Statistics (last 90 days):
╒═══════════════╤═══════════════╤═══════════════╤═══════════════╕
│ GPU Type      │ Median (hrs)  │ Mean (hrs)    │ Jobs Count    │
╞═══════════════╪═══════════════╪═══════════════╪═══════════════╡
│ A100-80GB     │ 2.3          │ 5.1          │ 1,234        │
│ V100-32GB     │ 1.8          │ 3.9          │ 567          │
│ RTX-6000      │ 0.9          │ 2.1          │ 890          │
╘═══════════════╧═══════════════╧═══════════════╧═══════════════╛
```

##### PI Group Reports

```bash
# Generate detailed report for specific PI group
python gpu_metrics.py pi_report --account=pi_smith_lab

# Include VRAM analysis
python gpu_metrics.py pi_report --account=pi_johnson_group --vram=True

# Aggregate view (summary only)
python gpu_metrics.py pi_report --account=pi_davis_team --aggregate=True

# Custom time period
python gpu_metrics.py pi_report --account=pi_wilson_lab --days_back=90
```

**Example Output**:
```
PI Report for pi_smith_lab (last 60 days):
================================================================================
📊 Summary:
• Total Jobs: 145
• Total GPU Hours: 2,847
• Average Efficiency: 67.3%
• Most Used GPU: A100-80GB (78% of jobs)

📈 Efficiency Breakdown:
• High Efficiency (>80%): 45 jobs (31%)
• Medium Efficiency (50-80%): 67 jobs (46%)
• Low Efficiency (<50%): 33 jobs (23%)

⏰ Wait Time Analysis:
• Average Queue Time: 2.4 hours
• Median Queue Time: 1.8 hours
• Jobs with >6hr wait: 12 (8%)
```

##### Efficiency Plotting

```bash
# Generate GPU efficiency plot
python gpu_metrics.py efficiency_plot

# Plot with constraints (multi-GPU jobs only)
python gpu_metrics.py efficiency_plot --constrs="GPUs >= 4"

# Custom title
python gpu_metrics.py efficiency_plot --title="Multi-GPU Job Efficiency"
```

##### Memory Usage Analysis

```bash
# Plot memory usage distribution
python gpu_metrics.py plot_mem_usage

# Focus on array jobs
python gpu_metrics.py plot_mem_usage --array=True

# Top 10% memory users
python gpu_metrics.py plot_mem_usage --top_pct=10

# Use VRAM buckets for analysis
python gpu_metrics.py plot_mem_usage --vram_buckets=True
```

### CPU Metrics (`cpu_metrics.py`)

Located in `src/analytics/`, this tool analyzes CPU-only jobs.

#### Basic Usage

```bash
cd src/analytics
python cpu_metrics.py [COMMAND] [OPTIONS]
```

#### Available Commands

##### Group Statistics

```bash
# Show CPU usage by PI group
python cpu_metrics.py group_stats

# Custom time period (6 months)
python cpu_metrics.py group_stats --days_back=182
```

**Example Output**:
```
CPU Usage by PI Group (last 182 days):
================================================================================
╒═══════════════════╤═══════════════╤═══════════════╤═══════════════╕
│ PI Group          │ CPU Hours     │ % of Total    │ Avg Job Hours │
╞═══════════════════╪═══════════════╪═══════════════╪═══════════════╡
│ pi_smith_lab      │ 45,678       │ 23.4%        │ 12.3         │
│ pi_johnson_group  │ 34,567       │ 17.8%        │ 8.7          │
│ pi_davis_team     │ 28,901       │ 14.9%        │ 15.2         │
│ pi_wilson_lab     │ 22,134       │ 11.4%        │ 6.9          │
╘═══════════════════╧═══════════════╧═══════════════╧═══════════════╛
```

##### PI Group Reports

```bash
# Detailed CPU report for specific group
python cpu_metrics.py pi_report --account=pi_smith_lab

# Custom time period
python cpu_metrics.py pi_report --account=pi_johnson_group --days_back=120
```

### Advanced GPU Metrics

For advanced analysis, you can use the standalone advanced metrics module:

```bash
cd src/analytics
python -c "
from advance_gpu_metrics import add_advanced_gpu_metrics
from gpu_metrics import GPUMetrics
import pandas as pd

# Load data
metrics = GPUMetrics()
df = metrics.df

# Add advanced metrics
df_enhanced = add_advanced_gpu_metrics(df)

# Show new columns
print('Advanced metrics added:')
print(df_enhanced[['gpu_utilization_efficiency', 'memory_utilization_ratio', 
                   'composite_underutilization_score']].head())
"
```

## 📧 Outreach Tools

### Email Outreach (`email_outreach.py`)

Located in `src/outreach/`, this tool identifies underutilized resources and generates outreach emails.

#### Basic Usage

```bash
cd src/outreach
python email_outreach.py [OPTIONS]
```

#### Command Options

##### Analysis Mode (Default)

```bash
# Basic analysis - show summary only
python email_outreach.py

# Custom time period
python email_outreach.py --days_back=90

# Custom thresholds
python email_outreach.py --min_wasted_jobs=5 --min_wasted_gb=10.0

# Stricter memory threshold (5% instead of 10%)
python email_outreach.py --memory_threshold=5
```

**Example Output**:
```
🎯 Email Outreach Analysis
📅 Analyzing last 60 days of data
📊 Criteria: ≥3 jobs, ≥4.0 GB wasted, <10% memory usage
================================================================================

📊 SUMMARY OF FLAGGED USERS:
• 12 users meet outreach criteria
• Total wasted GPU memory: 87.3 GB
• Total underutilized jobs: 45

👤 Top Users for Outreach:
1. researcher123: 8 jobs, 15.7 GB wasted
2. student456: 6 jobs, 12.3 GB wasted
3. postdoc789: 5 jobs, 9.8 GB wasted

💡 Recommendation: Focus outreach on top 5 users (represents 68% of waste)
```

##### Email Generation Mode

```bash
# Generate actual email content
python email_outreach.py --email=True

# With custom user list
python email_outreach.py --email=True --userlist=custom_users.csv

# Combined with custom thresholds
python email_outreach.py --email=True --min_wasted_jobs=5 --memory_threshold=5
```

**Example Email Output**:
```
================================================================================
👤 USER: researcher123 (John Smith)
📬 To: john.smith@university.edu

📊 Stats: 8 jobs, 15.7 GB wasted

📄 EMAIL CONTENT:
----------------------------------------
Subject: Optimizing Your GPU Usage on Unity

Dear John,

I hope this email finds you well. I'm reaching out regarding your recent GPU 
usage on the Unity cluster to help you optimize your computational work.

Over the past 60 days, we noticed that several of your GPU jobs used 
significantly less memory than requested:

• Job 12345: Used 1.2 GB out of 80 GB requested (1.5% utilization)
• Job 12346: Used 0.8 GB out of 80 GB requested (1.0% utilization)
• Job 12347: Used 2.1 GB out of 80 GB requested (2.6% utilization)

[Additional guidance and optimization suggestions...]
```

#### User Data Configuration

Create a CSV file for personalized emails:

```csv
username,email,first
john_doe,john.doe@university.edu,John
jane_smith,jane.smith@university.edu,Jane
researcher_bob,bob.wilson@university.edu,Bob
```

## 🔧 Utility Scripts

### Data Export (`export_to_csv.py`)

Located in `scripts/`, converts DuckDB data to CSV format.

```bash
cd scripts
python export_to_csv.py

# Custom output directory
python export_to_csv.py --output_dir=../data/processed/custom_export

# Export specific tables only
python export_to_csv.py --tables=jobs,users

# Custom database path
python export_to_csv.py --db_path=../data/raw/slurm_data_small.db
```

### Legacy Analysis (`zero_gpu_usage_list.py`)

Legacy tool for specific underutilization analysis:

```bash
cd scripts
python zero_gpu_usage_list.py

# Custom parameters
python zero_gpu_usage_list.py --days_back=90 --min_jobs=5
```

## 🎯 Common Usage Patterns

### Daily Monitoring Workflow

```bash
#!/bin/bash
# daily_monitoring.sh

cd /path/to/ds4cg-job-analytics

# Activate environment
source duckdb/bin/activate

# Generate daily reports
echo "=== Daily GPU Analytics ==="
cd src/analytics
python gpu_metrics.py waittime --days_back=1

echo "=== Outreach Analysis ==="
cd ../outreach
python email_outreach.py --days_back=7

echo "=== Export Daily Data ==="
cd ../../scripts
python export_to_csv.py --output_dir=../data/processed/daily_$(date +%Y%m%d)
```

### Weekly PI Reports

```bash
#!/bin/bash
# weekly_pi_reports.sh

PI_GROUPS=("pi_smith_lab" "pi_johnson_group" "pi_davis_team")

cd src/analytics
source ../../duckdb/bin/activate

for pi in "${PI_GROUPS[@]}"; do
    echo "=== Report for $pi ==="
    python gpu_metrics.py pi_report --account="$pi" --days_back=7 --vram=True
    echo ""
done
```

### Efficiency Analysis Pipeline

```bash
#!/bin/bash
# efficiency_analysis.sh

cd src/analytics
source ../../duckdb/bin/activate

# GPU efficiency analysis
echo "=== GPU Efficiency Analysis ==="
python gpu_metrics.py efficiency_plot
python gpu_metrics.py plot_mem_usage --vram_buckets=True

# CPU efficiency analysis  
echo "=== CPU Usage Analysis ==="
python cpu_metrics.py group_stats --days_back=30

# Identify optimization opportunities
echo "=== Optimization Opportunities ==="
cd ../outreach
python email_outreach.py --memory_threshold=15 --min_wasted_jobs=3
```

## 🔍 Advanced Usage

### Custom Database Paths

All tools support custom database paths:

```bash
# GPU metrics with custom DB
python gpu_metrics.py waittime --metricsfile=/path/to/custom.db

# CPU metrics with custom DB
python cpu_metrics.py group_stats --metricsfile=/path/to/custom.db

# Email outreach with custom DB
python email_outreach.py --dbfile=/path/to/custom.db
```

### Programmatic Usage

You can also use these tools programmatically:

```python
#!/usr/bin/env python3
"""
Custom analysis script
"""
import sys
sys.path.append('../src')

from analytics.gpu_metrics import GPUMetrics
from analytics.cpu_metrics import CPUMetrics
from outreach.email_outreach import main as email_main

# Load data
gpu_metrics = GPUMetrics(min_elapsed=600)
cpu_metrics = CPUMetrics(min_elapsed=600)

# Generate reports
gpu_metrics.waittime(days_back=30)
gpu_metrics.pi_report("pi_smith_lab", days_back=60)

cpu_metrics.group_stats(days_back=90)
cpu_metrics.pi_report("pi_smith_lab", days_back=60)

# Run outreach analysis
email_main(days_back=60, email=False)
```

### Batch Processing

For analyzing multiple time periods:

```bash
#!/bin/bash
# batch_analysis.sh

PERIODS=(7 14 30 60 90)

cd src/analytics
source ../../duckdb/bin/activate

for period in "${PERIODS[@]}"; do
    echo "=== Analysis for last $period days ==="
    python gpu_metrics.py waittime --days_back=$period > "waittime_${period}d.txt"
    python cpu_metrics.py group_stats --days_back=$period > "cpu_stats_${period}d.txt"
done
```

## 🆘 Troubleshooting

### Common Issues

!!! warning "Module Import Errors"
    **Problem**: `ModuleNotFoundError` when running scripts
    
    **Solution**:
    ```bash
    # Set Python path
    export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
    
    # Or run from correct directory
    cd src/analytics  # For analytics tools
    cd src/outreach   # For outreach tools
    ```

!!! warning "Database Connection Errors"
    **Problem**: Cannot connect to database
    
    **Solution**:
    ```bash
    # Check database exists
    ls data/raw/slurm_data_small.db
    
    # Check permissions
    chmod 644 data/raw/slurm_data_small.db
    
    # Use absolute path
    python gpu_metrics.py waittime --metricsfile=$(pwd)/data/raw/slurm_data_small.db
    ```

!!! warning "Empty Results"
    **Problem**: Commands return no data
    
    **Solutions**:
    - Increase `days_back` parameter
    - Check date range has data: `python -c "from analytics.gpu_metrics import GPUMetrics; print(GPUMetrics().df['StartTime'].min(), GPUMetrics().df['StartTime'].max())"`
    - Verify database is not empty

### Performance Tips

For large datasets:

```bash
# Use minimum elapsed time filter
python gpu_metrics.py waittime --min_elapsed=3600  # 1+ hour jobs only

# Limit time range for faster analysis
python gpu_metrics.py pi_report --account=pi_group --days_back=30

# Use constraints for focused analysis
python gpu_metrics.py efficiency_plot --constrs="GPUs >= 2"
```

### Getting Help

```bash
# Get help for any command
python gpu_metrics.py --help
python cpu_metrics.py --help
python email_outreach.py --help

# Check available methods
python -c "from analytics.gpu_metrics import GPUMetrics; help(GPUMetrics)"
```

The command-line tools are designed to be powerful yet easy to use. Combine them in scripts for automated analysis and reporting workflows that fit your specific needs!
