Module analytics.gpu_metrics
============================
gpu_metrics.py
-------------
This module provides functions and/or classes for analyzing GPU job metrics.

Typical functions may include:
    - Loading and filtering GPU job data
    - Calculating GPU utilization statistics
    - Reporting or visualizing GPU job usage

Update this docstring as you add or modify functions/classes in this file.

Functions
---------

`get_requested_vram(constraints)`
:   

Classes
-------

`GPUMetrics(metricsfile='../../data/raw/slurm_data_small.db', min_elapsed=600)`
:   A class for computing and plotting metrics about GPU jobs.
    
    Initialize metrics

    ### Methods

    `efficiency_plot(self, constrs=[], title='Used GPU VRAM by GPU Compute Hours')`
    :   Plot mem usage by compute hours.

    `pi_report(self, account, days_back=60, vram=False, aggregate=False)`
    :   Create an efficiency report for a given PI group.

    `plot_mem_usage(self, constrs=[], array=False, top_pct=10, vram_buckets=False, col='GPUMemUsage', **kwargs)`
    :   Plot memory usage

    `waittime(self, days_back=90, partition=None)`
    :   Get aggregate statistics on queue wait times by GPU.