"""
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
"""
import pandas as pd
import numpy as np

def gpu_utilization_efficiency(row):
    """
    Calculate the GPU Utilization Efficiency for a job.
    This is the ratio of actual GPU compute usage to the theoretical maximum possible,
    adjusted for job duration and number of GPUs requested.
    Returns NaN if Elapsed or GPUs is zero or missing.
    """
    if row['Elapsed'] > 0 and row['GPUs'] > 0:
        return row['GPUComputeUsage'] / (row['Elapsed'] * row['GPUs'])
    return np.nan

def memory_utilization_ratio(row, max_mem_per_gpu=16000):
    """
    Calculate the Memory Utilization Ratio for a job.
    This is the ratio of average GPU memory used to the total available GPU memory.
    max_mem_per_gpu: Maximum memory per GPU in MB (default 16000 MB).
    Returns NaN if GPUs is zero or missing.
    """
    if row['GPUs'] > 0:
        return row['GPUMemUsage'] / (row['GPUs'] * max_mem_per_gpu)
    return np.nan

def cpu_gpu_balance_score(row):
    """
    Calculate the CPU-GPU Balance Score for a job.
    This is the ratio of CPU compute usage to GPU compute usage.
    High values may indicate the job is CPU-bound rather than GPU-bound.
    Returns NaN if GPUComputeUsage is zero or missing.
    """
    if row['GPUComputeUsage'] > 0:
        return row['CPUComputeUsage'] / row['GPUComputeUsage']
    return np.nan

def gpu_request_discrepancy(row):
    """
    Calculate the GPU Request Discrepancy for a job.
    This is the difference between the number of GPUs requested and the actual usage per second.
    Returns NaN if Elapsed is zero or missing.
    """
    if row['Elapsed'] > 0:
        return row['GPUs'] - (row['GPUComputeUsage'] / row['Elapsed'])
    return np.nan

def composite_underutilization_score(row, max_mem_per_gpu=16000):
    """
    Calculate a Composite Underutilization Score for a job.
    This is a weighted combination of the above metrics for robust underutilization flagging.
    Weights can be tuned as needed. Returns NaN if all metrics are missing.
    """
    eff = gpu_utilization_efficiency(row)
    mem = memory_utilization_ratio(row, max_mem_per_gpu)
    bal = cpu_gpu_balance_score(row)
    disc = gpu_request_discrepancy(row)
    # Example weights: efficiency (0.4), memory (0.2), balance (0.2), discrepancy (0.2)
    score = 0
    count = 0
    if not np.isnan(eff):
        score += 0.4 * eff
        count += 0.4
    if not np.isnan(mem):
        score += 0.2 * mem
        count += 0.2
    if not np.isnan(bal):
        score += 0.2 * (1 / (1 + bal))  # Lower balance (less CPU-bound) is better
        count += 0.2
    if not np.isnan(disc):
        score += 0.2 * (1 - min(max(disc, 0), 1))  # Lower discrepancy is better
        count += 0.2
    return score / count if count > 0 else np.nan

def add_advanced_gpu_metrics(df, max_mem_per_gpu=16000):
    """
    Add all advanced GPU underutilization metrics as new columns to the DataFrame.
    max_mem_per_gpu: Maximum memory per GPU in MB (default 16000 MB).
    Returns a new DataFrame with additional metric columns.
    """
    df = df.copy()
    df['GPUUtilizationEfficiency'] = df.apply(gpu_utilization_efficiency, axis=1)
    df['MemoryUtilizationRatio'] = df.apply(memory_utilization_ratio, axis=1, max_mem_per_gpu=max_mem_per_gpu)
    df['CPUGPUBalanceScore'] = df.apply(cpu_gpu_balance_score, axis=1)
    df['GPURequestDiscrepancy'] = df.apply(gpu_request_discrepancy, axis=1)
    df['CompositeUnderutilizationScore'] = df.apply(composite_underutilization_score, axis=1, max_mem_per_gpu=max_mem_per_gpu)
    return df
