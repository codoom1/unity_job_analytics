Module analytics.cpu_metrics
============================
cpu_metrics.py
--------------
This module provides the CPUMetrics class for analyzing pure CPU jobs from a Slurm database.

Classes:
    - CPUMetrics: Methods for loading, filtering, and reporting on CPU job usage and statistics.

Usage:
    Run as a script with Fire to access command-line methods.

Classes
-------

`CPUMetrics(metricsfile='../../data/raw/slurm_data_small.db', min_elapsed=600, create_empty_db=False)`
:   A class for analyzing pure CPU jobs.
    
    Initialize metrics
    
    Args:
        metricsfile: Path to the DuckDB database file
        min_elapsed: Minimum elapsed time for jobs to be included (in seconds)
        create_empty_db: If True, create an empty database if the file doesn't exist

    ### Methods

    `group_stats(self, days_back=182)`
    :   Print the breakdown of CPU hour usage by PI group

    `pi_report(self, account, days_back=60)`
    :   Generate breakdown of CPU usage for PI group.