Module outreach.email_outreach
==============================
Email Outreach Tool for Underutilized GPU Jobs

This tool identifies users with underutilized GPU jobs and generates personalized
outreach emails similar to zero_gpu_usage_list.py but with enhanced functionality.

Functions
---------

`main(dbfile='../../data/raw/slurm_data_small.db', days_back=60, min_wasted_jobs=3, min_wasted_gb=4.0, memory_threshold=10, email=False, userlist='users.csv')`
:   Generate outreach emails for users with underutilized GPU jobs.
    
    Args:
        dbfile: Path to DuckDB database file
        days_back: Number of days to look back for job data
        min_wasted_jobs: Minimum number of wasted jobs to trigger outreach
        min_wasted_gb: Minimum GB of wasted GPU memory to trigger outreach
        memory_threshold: Memory usage threshold percentage (jobs below this are considered wasted)
        email: If True, generate and display emails; if False, just show summary
        userlist: Path to CSV file with user information (username, email, first_name)