# Outreach Module API Reference

The outreach module provides tools for identifying users with underutilized GPU resources and generating personalized outreach emails.

## Overview

This module helps system administrators and research computing staff:

- Identify users consistently underutilizing GPU resources
- Generate personalized emails with specific usage statistics
- Create comprehensive reports for resource optimization

## Email Outreach Tool

::: src.outreach.email_outreach
    options:
      show_source: true
      show_root_heading: true
      heading_level: 3

## Email Templates

::: src.outreach.email_templates
    options:
      show_source: true
      show_root_heading: true
      heading_level: 3

## Usage Examples

### Basic Usage

```python
from outreach.email_outreach import main

# Analyze last 60 days, show summary only
main(days_back=60, email=False)

# Generate actual email content
main(days_back=60, email=True)
```

### Custom Thresholds

```python
# More restrictive criteria
main(
    days_back=90,
    min_wasted_jobs=5,      # At least 5 underutilized jobs
    min_wasted_gb=10.0,     # At least 10 GB wasted
    memory_threshold=5,      # Less than 5% memory usage
    email=True
)
```

### Command Line Usage

The outreach tool can be used from the command line:

```bash
cd src/outreach

# Basic analysis
python email_outreach.py

# With custom parameters
python email_outreach.py --days_back=90 --min_wasted_jobs=5 --email=True

# Using custom user list
python email_outreach.py --userlist=custom_users.csv --email=True
```

### Email Template Examples

```python
from outreach.email_templates import generate_email, generate_comprehensive_email

# Simple email
user_jobs = [{'JobID': 12345, 'GPUMemUsage': 1.2e9}]
email_content = generate_email("john_doe", user_jobs)

# Comprehensive email (matches zero_gpu_usage_list.py format)
user_data = {
    'WastedJobs': 8,
    'TotalWastedGB': 15.7,
    'WastedGPUHours': 196.25
}
job_samples = [
    {'JobID': 12345, 'GPUMemUsage': 1.2e9},
    {'JobID': 12346, 'GPUMemUsage': 0.8e9}
]
email = generate_comprehensive_email("John Smith", user_data, job_samples)
```

## Configuration

### User Data File

Create a CSV file with user information for personalized emails:

```csv
username,email,first
john_doe,john.doe@university.edu,John
jane_smith,jane.smith@university.edu,Jane
researcher_bob,bob.wilson@university.edu,Bob
```

### Thresholds Explained

| Parameter | Description | Recommended Values |
|-----------|-------------|-------------------|
| `days_back` | Analysis timeframe | 30-90 days |
| `min_wasted_jobs` | Minimum underutilized jobs | 3-5 jobs |
| `min_wasted_gb` | Minimum wasted GPU memory | 4-10 GB |
| `memory_threshold` | Max memory usage % to be considered "wasted" | 5-15% |

### Output Examples

#### Summary Output
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
```

#### Email Content Example
```
Subject: Optimizing Your GPU Usage on Unity

Dear John,

I hope this email finds you well. I'm reaching out regarding your recent GPU usage on the Unity cluster to help you optimize your computational work.

Over the past 60 days, we noticed that several of your GPU jobs used significantly less memory than requested:

• Job 12345: Used 1.2 GB out of 80 GB requested (1.5% utilization)
• Job 12346: Used 0.8 GB out of 80 GB requested (1.0% utilization)

This represents approximately 15.7 GB of underutilized GPU memory across 8 jobs.

[Additional guidance and resources...]
```

## Integration with Analytics

The outreach module works seamlessly with the analytics module:

```python
from analytics.gpu_metrics import GPUMetrics
from outreach.email_outreach import main

# Use same database for consistency
metrics = GPUMetrics(metricsfile="data/slurm_data_small.db")
print(f"Loaded {len(metrics.df)} GPU jobs")

# Run outreach analysis on same data
main(dbfile="data/slurm_data_small.db", email=True)
```

## Best Practices

### For System Administrators

1. **Regular monitoring**: Run weekly/monthly to catch patterns early
2. **Graduated approach**: Start with higher thresholds, then tighten
3. **Educational focus**: Frame as optimization help, not criticism
4. **Follow-up**: Track whether users improve after outreach

### Customizing Email Content

```python
# Modify templates in email_templates.py
INTRO = """
Dear {user_name},

Your customized introduction here...
"""

# Add institution-specific resources
RESOURCES = """
For help optimizing your code:
- Workshop: "GPU Programming Basics" - Fridays 2-4 PM
- Documentation: https://your-hpc.edu/gpu-guide
- Office hours: Tuesdays 10-12 PM in Computer Center
"""
```

### Avoiding False Positives

```python
# Exclude specific job types that legitimately use little memory
main(
    days_back=60,
    min_wasted_jobs=5,      # Higher threshold
    memory_threshold=5,      # Lower threshold (more strict)
    email=False             # Review before sending
)
```

## Error Handling

The outreach module includes robust error handling:

- **Database connectivity**: Clear messages for connection issues
- **Missing user data**: Graceful handling of missing user information
- **Date filtering**: Automatic fallback when no recent data exists
- **Email generation**: Handles missing job details gracefully

## Privacy and Ethics

!!! warning "User Privacy"
    - Only authorized personnel should run outreach analysis
    - Ensure compliance with institutional privacy policies
    - Consider opt-out mechanisms for users

!!! tip "Constructive Approach"
    - Frame outreach as educational opportunity
    - Provide specific, actionable recommendations
    - Offer resources and support for optimization
