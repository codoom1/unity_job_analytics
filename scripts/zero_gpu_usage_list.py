import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import duckdb
import pandas as pd
from fire import Fire
from datetime import datetime, timedelta
from src.analytics.gpu_metrics import GPUMetrics

INTRO = """Dear {name},

Over the past few months, we've noticed that all of your {jobs} jobs on Unity which requested GPU resources did not utilize the requested GPUs."""

HOURS = "{hours} unused GPU hours. The most recent jobs are the following:"

def get_job_type_breakdown(interactive, jobs):
  if interactive == jobs:
     return f" These consisted of {interactive} interactive sessions, totaling "
  elif not interactive:
     return " These amounted to "
  else:
     return f" These included {interactive} interactive session{'s' if interactive > 1 else ''}, as well as {jobs-interactive} batch job{'s' if jobs-interactive>1 else ''}, totaling "


def pi_report(account, days_back=60):
    """Create an efficiency report for a given PI group."""
    # Note: This function seems incomplete as 'df' is not defined
    # You may need to pass df as a parameter or get it from GPUMetrics
    
    cutoff = datetime.now() - timedelta(days=days_back)
    
    # First try with date filter
    try:
        filtered_df = duckdb.query(
            "select GPUs*Elapsed/3600 as GPUHours, GPUMemUsage=0 as Wasted, GPUMemUsage, Interactive,"
            f"User, Queued from df where Account='{account}' and StartTime>='{cutoff}'"
        ).df()
    except NameError:
        print("Error: 'df' not defined. This function needs to be called with proper context.")
        return
        
    # If no data found, try without date filter
    if filtered_df.empty:
        print(f"No data found for account '{account}' in last {days_back} days, using all available data...")
        filtered_df = duckdb.query(
            "select GPUs*Elapsed/3600 as GPUHours, GPUMemUsage=0 as Wasted, GPUMemUsage, Interactive,"
            f"User, Queued from df where Account='{account}'"
        ).df()
    filtered_df["Queued"] = filtered_df["Queued"].apply(lambda x: x.total_seconds()/3600)
    filtered_df["WastedHours"] = filtered_df["GPUHours"] * filtered_df["Wasted"]
    filtered_df["Interactive" ] = filtered_df["Interactive"].notna()
    filtered_df["GPUMemUsage"] /= 2**30
    gb = filtered_df.groupby(["User", "Wasted"])
    print(gb.mean()[["GPUHours", "GPUMemUsage", "Queued"]].rename(columns={"Wasted": "Fraction "}))

def main(dbfile="../data/raw/slurm_data_small.db", userlist="/work/pi_bpachev_umass_edu/reporting/slurm-analytics/users.csv", email=False, days_back=60):
    """Print out a list of users who habitually waste GPU hours."""

    metrics = GPUMetrics(metricsfile=dbfile)
    jobs = metrics.df

    cutoff = datetime.now() - timedelta(days=days_back)
    
    # First try with date filter
    df = duckdb.query(
        "select GPUs*Elapsed/3600 as GPUHours, GPUMemUsage=0 as Wasted, GPUMemUsage, Interactive,"
        f"User, Queued, IsArray, Account, StartTime, JobID, Status from jobs where StartTime>='{cutoff}' "
        " and (Status = 'COMPLETED' or Status = 'TIMEOUT')"
    ).df()
    
    # If no data found, try without date filter
    if df.empty:
        print(f"No data found in last {days_back} days, using all available data...")
        df = duckdb.query(
            "select GPUs*Elapsed/3600 as GPUHours, GPUMemUsage=0 as Wasted, GPUMemUsage, Interactive,"
            "User, Queued, IsArray, Account, StartTime, JobID, Status from jobs where "
            " (Status = 'COMPLETED' or Status = 'TIMEOUT')"
        ).df()
    df["WastedGPUHours"] = df["Wasted"] * df["GPUHours"]
    df["Interactive"] = df["Interactive"].notna()
    print(df['Status'].unique())
    gb = df.groupby("User")
    
    user_report = gb[["Wasted", "WastedGPUHours", "GPUHours", "IsArray", "Interactive"]].sum()
    user_report["TotalJob"] = gb.size()
    user_report["WasteRatio"] = user_report["WastedGPUHours"] / user_report["GPUHours"]
    user_report["PI"] = gb["Account"].first()
    user_report["LastJob"] = gb["StartTime"].max()
    mask = (user_report["Wasted"] > 3) & (user_report["WastedGPUHours"] > 4)
    filtered_report = user_report[mask].reset_index().sort_values("WasteRatio")
    sorted_report = filtered_report[filtered_report["WasteRatio"] == 1].sort_values("WastedGPUHours", ascending=False).reset_index(drop=True)
    sorted_report["H/J"] = sorted_report["WastedGPUHours"] / sorted_report["Wasted"]

    users = pd.read_csv(userlist).set_index("username")

    if email:
        for idx, row in sorted_report.iterrows():
            interactive = int(row["Interactive"])
            jobs = int(row["Wasted"])
            template = INTRO+get_job_type_breakdown(interactive, jobs)+HOURS
            user_info = users.loc[row["User"]]
            name = user_info["first"]
            email = template.format(name=name, jobs=jobs, hours=int(row["WastedGPUHours"]))
            job_samples = duckdb.query(
                    "select JobID as Job, StartTime as Start, GPUHours from df "
                    f" where User='{row['User']}' order by StartTime desc limit 5"
                    ).df()
            print(user_info["email"])
            print(email+'\n')
            print(job_samples.rename(columns={"GPUHours": "Unused GPU Hours"}).to_string(index=False))
    else:
        print(sorted_report[["User", "Wasted", "WastedGPUHours", "H/J", "LastJob"]].rename(
          columns={"Wasted":"Jobs", "WastedGPUHours":"Hours"}
        ).to_markdown(tablefmt="grid", floatfmt=".1f"))

if __name__ == "__main__":
    Fire(main)
