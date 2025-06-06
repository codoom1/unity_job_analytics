Module analytics.advance_gpu_metrics
====================================
advance_gpu_metrics.py
---------------------
This module provides advanced metrics for analyzing GPU job underutilization in HPC or cloud environments.

Functions:
    - gpu_utilization_efficiency: Measures how efficiently requested GPU resources were used.
    - memory_utilization_ratio: Measures the ratio of GPU memory used to total available memory.
    - cpu_gpu_balance_score: Indicates if a job is CPU-bound while underutilizing GPU.
    - gpu_request_discrepancy: Quantifies the difference between GPUs requested and actual usage.
    - composite_underutilization_score: Combines multiple metrics into a single underutilization score.
    - add_advanced_gpu_metrics: Adds all advanced metrics as columns to a DataFrame.

All functions assume the input DataFrame has columns: 'Elapsed', 'GPUs', 'GPUComputeUsage', 'GPUMemUsage', 'CPUComputeUsage'.

Functions
---------

`add_advanced_gpu_metrics(df, max_mem_per_gpu=16000)`
:   Add all advanced GPU underutilization metrics as new columns to the DataFrame.
    max_mem_per_gpu: Maximum memory per GPU in MB (default 16000 MB).
    Returns a new DataFrame with additional metric columns.

`composite_underutilization_score(row, max_mem_per_gpu=16000)`
:   Calculate a Composite Underutilization Score for a job.
    This is a weighted combination of the above metrics for robust underutilization flagging.
    Weights can be tuned as needed. Returns NaN if all metrics are missing.

`cpu_gpu_balance_score(row)`
:   Calculate the CPU-GPU Balance Score for a job.
    This is the ratio of CPU compute usage to GPU compute usage.
    High values may indicate the job is CPU-bound rather than GPU-bound.
    Returns NaN if GPUComputeUsage is zero or missing.

`gpu_request_discrepancy(row)`
:   Calculate the GPU Request Discrepancy for a job.
    This is the difference between the number of GPUs requested and the actual usage per second.
    Returns NaN if Elapsed is zero or missing.

`gpu_utilization_efficiency(row)`
:   Calculate the GPU Utilization Efficiency for a job.
    This is the ratio of actual GPU compute usage to the theoretical maximum possible,
    adjusted for job duration and number of GPUs requested.
    Returns NaN if Elapsed or GPUs is zero or missing.

`memory_utilization_ratio(row, max_mem_per_gpu=16000)`
:   Calculate the Memory Utilization Ratio for a job.
    This is the ratio of average GPU memory used to the total available GPU memory.
    max_mem_per_gpu: Maximum memory per GPU in MB (default 16000 MB).
    Returns NaN if GPUs is zero or missing.