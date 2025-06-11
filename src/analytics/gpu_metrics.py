"""
gpu_metrics.py
-------------
This module provides functions and/or classes for analyzing GPU job metrics.

Typical functions may include:
    - Loading and filtering GPU job data
    - Calculating GPU utilization statistics
    - Reporting or visualizing GPU job usage

Update this docstring as you add or modify functions/classes in this file.
"""

import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime, timedelta
from fire import Fire

ram_map = {'a100': 80, 'v100': 16, 'a40': 48, 'gh200':95,
           'rtx_8000': 48, '2080_ti': 11, '1080_ti': 11, '2080': 8,
           'h100': 80, 'l4': 23, 'm40': 23, 'l40s': 48, 'titan_x': 12, 'a16': 16
          }

vram_cutoffs = [-1, 1e-6, 8, 11, 12, 16, 23, 32, 40, 48, 80]
vram_labels = [0] + vram_cutoffs[2:]

def get_requested_vram(constraints):
    try:
        nconstrs = len(constraints)
    except:
        return 0
    requested_vrams = []
    for constr in constraints:
        constr = constr.strip("'")
        if constr.startswith('vram'):
            requested_vrams.append(int(constr.replace('vram','')))
        elif constr.startswith('gpu'):
            gpu_type = constr.split(':')[1]
            requested_vrams.append(ram_map[gpu_type])
    if not(len(requested_vrams)): return 0
    else: return min(requested_vrams)


class GPUMetrics:
    """A class for computing and plotting metrics about GPU jobs."""
    
    def __init__(self,
                 metricsfile=None,
                 min_elapsed=600
                ):
        """Initialize metrics"""
        
        # If no metricsfile is provided, use default path relative to script location
        if metricsfile is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(script_dir))
            metricsfile = os.path.join(project_root, "data", "raw", "slurm_data.db")
        
        self.con = duckdb.connect(metricsfile)
        # TODO - handle array jobs properly
        df = self.con.query(
            "select GPUs,GPUType, GPUMemUsage, GPUComputeUsage,CPUs, CPUMemUsage, CPUComputeUsage, Elapsed, "
            "StartTime,"
            "StartTime-SubmitTime as Queued, TimeLimit, Interactive, "
            "IsArray, JobID, ArrayID, Status, Constraints, Partition, User, Account from Jobs "
            f"where GPUs > 0 and Elapsed>{int(min_elapsed)} and GPUType is not null "
            " and Status != 'CANCELLED' and Status != 'FAILED'"
        ).to_df()

        ## Here we should include Cancelled and Failed jobs, but we need to handle them properly.
        ## Why the Elapsed time is so short? or less than 10 minutes?
        ## This compute the requested VRAM for each job based on constraints.
        ## And how does contraints relate to requested VRAM?
        df["requested_vram"] = df["Constraints"].apply(lambda c: get_requested_vram(c))
        
        df["allocated_vram"] = df["GPUType"].apply(lambda x: min(ram_map[t] for t in x))
        df["user_jobs"] = df.groupby("User")["User"].transform('size')
        df["account_jobs"] = df.groupby("Account")["Account"].transform('size')
        self.df = df

    def plot_mem_usage(self, constrs=[], array=False, top_pct=10, vram_buckets=False,
        col="GPUMemUsage",
        **kwargs
    ):
        """Plot memory usage"""

        plot_args = {"bins": 80, "title": "GPU Memory Usage for Unity Jobs"}
        plot_args.update(kwargs)
        if array: constrs.append("IsArray>0")
        else: constrs.append("not IsArray")
        df = self.df
        new_df = duckdb.query(f"select {col}, User from df where " + (" and ".join(constrs))).df()

        new_df["UserRank"] = new_df["User"].map(new_df["User"].value_counts().rank(pct=True))
        thresh = (100-top_pct) /100
        plotting_df = pd.DataFrame(
            {
                f"Top {top_pct}% of users": new_df[col][new_df["UserRank"]>thresh],
                f"Bottom {100-top_pct}% of users": new_df[col][new_df["UserRank"]<=thresh]            
            })
        if col == "GPUMemUsage":
            plotting_df = (plotting_df / 2**30).clip(0, 95)
        if vram_buckets or col != "GPUMemUsage":
            plotting_df = pd.DataFrame({
                x:  pd.cut(plotting_df[x], bins=vram_cutoffs, labels=vram_labels).value_counts().sort_index()
                for x in plotting_df.columns
            })
            print(plotting_df)
            plotting_df.plot.bar(
                stacked=True
            )
            xlabel = "Min needed VRAM Constraint" if col == "GPUMemUsage" else "VRAM (G)"
            plt.xlabel(xlabel)
        else:
            plotting_df.plot.hist(bins=plot_args["bins"], stacked=True)
            plt.xlabel("Memory Usage in Gigabytes")

        plt.title(plot_args["title"])
        plt.ylabel("#Jobs")
        plt.show()
        print(plotting_df.describe())

    def efficiency_plot(self, constrs=[], title="Used GPU VRAM by GPU Compute Hours"):
        """Plot mem usage by compute hours."""

        df = self.df
        if len(constrs):
            where = "where " + (" and ".join(constrs))
        else:
            where = ""
        filtered_df = duckdb.query(
            f"select GPUs, GPUMemUsage, Elapsed, requested_vram, IsArray"
            ", Elapsed*GPUs/3600 as gpu_hours "
            " from df " + where 
        ).df()
        filtered_df["used_vram"] = pd.cut(filtered_df["GPUMemUsage"]/2**30, labels=vram_labels, bins=vram_cutoffs)
        #filtered_df.groupby(["requested_vram", "IsArray"])["gpu_hours"].sum()
        filtered_df.loc[(filtered_df["used_vram"]==12), "used_vram"] = 11
        filtered_df.loc[(filtered_df["used_vram"]==16), "used_vram"] = 23
        tot_hours = filtered_df.groupby(["used_vram"], observed=False)["gpu_hours"].sum().reset_index()
        tot_hours = tot_hours[tot_hours["gpu_hours"] >0]
        tot_hours.plot.pie(
            figsize=(9,9), legend=False,
            y='gpu_hours', labels=[f"{i}G" for i in tot_hours["used_vram"]], autopct='%1.1f%%')
        #tot_hours.plot.pie()
        plt.ylabel('')
        plt.title(title)
        plt.show()
    
    def pi_report(self, account, days_back=60, vram=False, aggregate=False):
        """Create an efficiency report for a given PI group."""

        df = self.df
        cutoff = datetime.now() - timedelta(days=days_back)
        
        # First try with date filter
        filtered_df = duckdb.query(
            "select GPUs*Elapsed/3600 as GPUHours, GPUMemUsage=0 as Wasted, GPUMemUsage, Interactive,"
            "requested_vram as ReqVRAM, allocated_vram as AllocVRAM,"
            f"User, Queued from df where Account='{account}' and StartTime>='{cutoff}'"
        ).df()
        
        # If no data found, try without date filter
        if filtered_df.empty:
            print(f"No data found for account '{account}' in last {days_back} days, using all available data...")
            filtered_df = duckdb.query(
                "select GPUs*Elapsed/3600 as GPUHours, GPUMemUsage=0 as Wasted, GPUMemUsage, Interactive,"
                "requested_vram as ReqVRAM, allocated_vram as AllocVRAM,"
                f"User, Queued from df where Account='{account}'"
            ).df()
        filtered_df["Queued"] = filtered_df["Queued"].apply(lambda x: x.total_seconds()/3600)
        filtered_df["WastedHours"] = filtered_df["GPUHours"] * filtered_df["Wasted"]
        filtered_df["Interactive" ] = filtered_df["Interactive"].notna()
        filtered_df["GPUMemUsage"] /= 2**30
        if aggregate:
            gb = filtered_df
        else:
            gb = filtered_df.groupby(["User"])
        summary = gb[["GPUHours", "WastedHours"]].sum()
        summary["Mean Queued Hours"] = gb["Queued"].mean()
        summary["# jobs"] = gb["Queued"].count()
        summary["% wasted"] = summary["WastedHours"]/summary["GPUHours"] * 100
        print(f"GPU usage for PI group {account}")
        if aggregate:
            print(summary.rename({"GPUHours": "Total GPU Hours", "WastedHours": "Wasted GPU Hours"}).to_markdown(tablefmt="grid", floatfmt=".1f", headers=[]))
        else:
            print(summary["% wasted"].describe())
            print(summary.rename(columns={"GPUHours": "Total GPU Hours", "WastedHours": "Wasted GPU Hours"}).to_markdown(tablefmt="grid", floatfmt=".1f"))

        if vram:
            print("VRAM breakdown")
            vramdf = gb[["GPUMemUsage", "ReqVRAM"]].describe()
            if aggregate:
                print(vramdf)
                print(vramdf[['count','mean','25%','50%','75%','max']].to_markdown(tablefmt="grid", floatfmt=".1f"))
            else:
                vramdf = vramdf.sort_values("count").iloc[-1:-11:-1]
            #print(vramdf.sort_values("count").iloc[::-1])
                print(vramdf[['count','mean','25%','50%','75%','max']].to_markdown(tablefmt="grid", floatfmt=".1f"))

    def waittime(self, days_back=90, partition=None):
        """Get aggregate statistics on queue wait times by GPU."""

        df = self.df
        cutoff = datetime.now() - timedelta(days=days_back)
        partition_constr = "" if partition is None else f" and Partition='{partition}'"
        
        # First try with the date filter
        filtered_df = duckdb.query(
            "select Interactive, GPUType[1] as GPUType, "
            f"Queued from df where StartTime>='{cutoff}'" + partition_constr
        ).df()
        
        # If no data found, try without date filter
        if filtered_df.empty:
            print(f"No data found in last {days_back} days, using all available data...")
            filtered_df = duckdb.query(
                "select Interactive, GPUType[1] as GPUType, "
                f"Queued from df where 1=1" + partition_constr
            ).df()
        print(filtered_df)
        filtered_df["Queued"] = filtered_df["Queued"].apply(lambda x: x.total_seconds()/3600)
        gb = filtered_df.groupby("GPUType")
        summary = gb["Queued"].describe()
        print(summary.to_markdown(tablefmt="grid", floatfmt=".1f"))
        print(gb[["Queued"]].median().rename(columns={"Queued": "Median Queued Hours"}).to_markdown(tablefmt="grid", floatfmt=".1f"))

if __name__ == "__main__":
    Fire(GPUMetrics)
