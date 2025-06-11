# Analytics Module API Reference

This module contains the core analytics functionality for analyzing GPU and CPU job metrics from the SLURM database.

## Overview

The analytics module provides two main classes:

- **`GPUMetrics`**: For analyzing GPU job utilization, wait times, and efficiency
- **`CPUMetrics`**: For analyzing CPU-only job usage patterns

## GPU Metrics

::: src.analytics.gpu_metrics
    options:
      show_source: true
      show_root_heading: true
      heading_level: 3

## CPU Metrics  

::: src.analytics.cpu_metrics
    options:
      show_source: true
      show_root_heading: true
      heading_level: 3

## Advanced GPU Metrics

::: src.analytics.advance_gpu_metrics
    options:
      show_source: true
      show_root_heading: true
      heading_level: 3

## Usage Examples

### Basic GPU Analysis

```python
from analytics.gpu_metrics import GPUMetrics

# Load GPU job data
metrics = GPUMetrics(min_elapsed=600)  # Jobs > 10 minutes

# Get wait time statistics
metrics.waittime(days_back=30)

# Generate PI group report
metrics.pi_report("pi_smith_lab", days_back=60)

# Create efficiency plot
metrics.efficiency_plot()
```

### CPU Analysis

```python
from analytics.cpu_metrics import CPUMetrics

# Load CPU job data
cpu = CPUMetrics(min_elapsed=600)

# Group statistics
cpu.group_stats(days_back=180)

# PI-specific report
cpu.pi_report("pi_johnson_group")
```

### Advanced Metrics

```python
from analytics.advance_gpu_metrics import add_advanced_gpu_metrics
import pandas as pd

# Add advanced utilization metrics to your DataFrame
df_with_metrics = add_advanced_gpu_metrics(gpu_jobs_df)

# Now you have additional columns:
# - gpu_utilization_efficiency
# - memory_utilization_ratio  
# - cpu_gpu_balance_score
# - gpu_request_discrepancy
# - composite_underutilization_score
```

## Common Parameters

### Time Filtering

Most methods accept `days_back` parameter to limit analysis timeframe:

```python
# Last 30 days
metrics.waittime(days_back=30)

# Last 6 months  
metrics.pi_report("pi_group", days_back=180)
```

### Database Configuration

```python
# Custom database path
metrics = GPUMetrics(metricsfile="path/to/database.db")

# Minimum job duration filter (seconds)
metrics = GPUMetrics(min_elapsed=3600)  # Jobs > 1 hour
```

## Error Handling

The analytics modules include robust error handling:

- **Missing data**: Automatically falls back to all available data when date filters return empty results
- **Database connection**: Clear error messages for connection issues  
- **Invalid parameters**: Validation of input parameters with helpful error messages

## Performance Tips

### For Large Datasets

```python
# Use larger min_elapsed to focus on significant jobs
metrics = GPUMetrics(min_elapsed=3600)  # 1+ hour jobs only

# Limit analysis timeframe
metrics.waittime(days_back=30)  # Recent data only

# Use constraints for plotting
metrics.efficiency_plot(constrs=['GPUs >= 4'])  # Multi-GPU jobs only
```

### Memory Optimization

```python
# For memory-efficient analysis
import gc

metrics = GPUMetrics()
result = metrics.waittime()
del metrics  # Free memory
gc.collect()
```
