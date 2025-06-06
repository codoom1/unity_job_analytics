"""
cpu_metrics.py
--------------
This module provides the CPUMetrics class for analyzing pure CPU jobs from a Slurm database.

Classes:
    - CPUMetrics: Methods for loading, filtering, and reporting on CPU job usage and statistics.

Usage:
    Run as a script with Fire to access command-line methods.
"""

import duckdb
from datetime import datetime, timedelta
import pandas as pd
from fire import Fire
import numpy as np

class CPUMetrics:
    """A class for analyzing pure CPU jobs."""

    def __init__(self,
                 metricsfile="../../data/raw/slurm_data_small.db",
                 min_elapsed=600,
                 create_empty_db=False):
        """Initialize metrics
        
        Args:
            metricsfile: Path to the DuckDB database file
            min_elapsed: Minimum elapsed time for jobs to be included (in seconds)
            create_empty_db: If True, create an empty database if the file doesn't exist
        """
        
        try:
            self.con = duckdb.connect(metricsfile)
        except Exception as e:
            if create_empty_db:
                print(f"Creating empty database at {metricsfile}")
                self.con = duckdb.connect(metricsfile)
                self.con.execute("""
                CREATE TABLE Jobs (
                    Elapsed INT, 
                    StartTime TIMESTAMP, 
                    CPUs INT,
                    SubmitTime TIMESTAMP,
                    TimeLimit INT,
                    Interactive BOOLEAN,
                    IsArray BOOLEAN,
                    JobID INT,
                    ArrayID INT,
                    Status VARCHAR,
                    Constraints VARCHAR,
                    Partition VARCHAR,
                    User VARCHAR,
                    Account VARCHAR
                )
                """)
                # Add sample data or return early
                print("Created empty database. Add sample data before running analyses.")
                self.df = pd.DataFrame(columns=[
                    "Elapsed", "StartTime", "CPUs", "Queued", "TimeLimit", 
                    "Interactive", "IsArray", "JobID", "ArrayID", "Status", 
                    "Constraints", "Partition", "User", "Account"
                ])
                return
            else:
                print(f"Error accessing database: {e}")
                print("Use --create_empty_db=True to create an empty database")
                self.df = pd.DataFrame()
                return
        # TODO - handle array jobs properly
        df = self.con.query(
            "select Elapsed, StartTime, CPUs,"
            "StartTime-SubmitTime as Queued, TimeLimit, Interactive, "
            "IsArray, JobID, ArrayID, Status, Constraints, Partition, User, Account from Jobs "
            f"where Elapsed>{int(min_elapsed)} "
            " and Status != 'CANCELLED' and Status != 'FAILED'"
        ).to_df()
        self.df = df
  
    def group_stats(self, days_back=182):
        """Print the breakdown of CPU hour usage by PI group"""
        df = self.df
        cutoff = datetime.now() - timedelta(days=days_back)
        filtered_df = duckdb.query(
                "select sum(CPUs*Elapsed/3600) as CPUHours, Account from df group by Account"
                ).df()
        print(filtered_df["CPUHours"].describe().to_markdown(tablefmt="grid", floatfmt=".1f"))
        total_cpu_hours = filtered_df["CPUHours"].sum()
        filtered_df["CPUHours"] /= total_cpu_hours
        sorted_df = filtered_df.sort_values("CPUHours").iloc[::-1]
        sorted_arr = sorted_df["CPUHours"].values
        quantiles = [.5, .6, .7, .8, .9, .99]
        cutoffs = np.cumsum(sorted_arr)
        print(quantiles, np.searchsorted(cutoffs, quantiles))

    def pi_report(self, account, days_back=60):
        """Generate breakdown of CPU usage for PI group."""
        df = self.df
        cutoff = datetime.now() - timedelta(days=days_back)
        
        # First try with date filter
        filtered_df = duckdb.query(
            "select CPUs*Elapsed/3600 as CPUHours, CPUs, Interactive,"
            f"User, Queued from df where Account='{account}' and StartTime>='{cutoff}'"
        ).df()
        
        # If no data found, try without date filter
        if filtered_df.empty:
            print(f"No data found for account '{account}' in last {days_back} days, using all available data...")
            filtered_df = duckdb.query(
                "select CPUs*Elapsed/3600 as CPUHours, CPUs, Interactive,"
                f"User, Queued from df where Account='{account}'"
            ).df()
        filtered_df["Queued"] = filtered_df["Queued"].apply(lambda x: x.total_seconds()/3600)
        filtered_df["Interactive" ] = filtered_df["Interactive"].notna()
        gb = filtered_df.groupby(["User"])
        print(f"CPU usage for PI group {account}")
        summary = gb[["CPUs", "Queued"]].median()
        summary["Total CPU Hours"] = gb["CPUHours"].sum()
        summary["Pct Usage"] = summary["Total CPU Hours"]/summary["Total CPU Hours"].sum() * 100
        summary["# of jobs"] = gb["CPUs"].count()
        summary["Max CPUs"] = gb["CPUs"].max()
        print(summary.rename(columns={"CPUs": "Median CPUs/job", "Queued": "Median queued hours"}).to_markdown(tablefmt="grid", floatfmt=".1f"))

if __name__ == "__main__":
    Fire(CPUMetrics)
