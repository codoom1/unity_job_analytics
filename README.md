# SLURM Job Analytics Project

A comprehensive data science project for analyzing GPU and CPU job utilization on Unity HPC cluster.

## 📁 Project Structure

```
├── data/
│   ├── raw/                    # Raw database files
│   │   └── slurm_data_small.db
│   └── processed/              # Processed/exported data
│       └── csv_output/
├── src/                        # Source code
│   ├── analytics/              # Core analytics modules
│   │   ├── gpu_metrics.py      # GPU job analysis
│   │   └── cpu_metrics.py      # CPU job analysis
│   ├── dashboard/              # Streamlit web dashboard
│   │   └── app.py
│   └── outreach/               # Email outreach functionality
│       ├── email_templates.py  # Email templates
│       └── email_outreach.py   # Outreach tool
├── scripts/                    # Utility scripts
│   ├── export_to_csv.py        # Database export
│   └── zero_gpu_usage_list.py  # Legacy analysis
├── notebooks/                  # Jupyter notebooks
│   └── SlurmGPU.ipynb
├── docs/                       # Documentation
│   └── DATE_FILTERING_FIXES.md
└── tests/                      # Test files
```

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Create and activate virtual environment
python -m venv duckdb && source duckdb/bin/activate

# Run setup script (recommended)
python setup.py

# OR install manually
pip install -r requirements.txt
```

### 2. Run Dashboard

```bash
cd src/dashboard
streamlit run app.py
```

The dashboard will be available at `http://localhost:8501` with:

- **GPU Analytics**: Wait times, efficiency metrics, utilization patterns
- **CPU Analytics**: Resource usage by user and group
- **Email Outreach**: Automated flagging and email generation for underutilized resources

### 3. Command Line Tools

#### GPU Analytics

```bash
cd src/analytics
python gpu_metrics.py waittime                    # Queue wait time analysis
python gpu_metrics.py pi_report --account=pi_name # PI group report
python gpu_metrics.py efficiency_plot                # GPU utilization efficiency
```

#### CPU Analytics

```bash
cd src/analytics
python cpu_metrics.py group_stats                 # Group usage statistics
python cpu_metrics.py pi_report --account=pi_name # PI group CPU report
```

#### Email Outreach

```bash
cd src/outreach
python email_outreach.py                          # Analyze and flag users
python email_outreach.py --email=True             # Generate email content
python email_outreach.py --min_wasted_jobs=10     # Custom thresholds
```

#### Data Export

```bash
cd scripts
python export_to_csv.py                           # Export DuckDB to CSV
```

## 📊 Features

### Analytics Dashboard
- **Interactive Web Interface**: Streamlit-based dashboard for real-time analysis
- **GPU/CPU Metrics**: Comprehensive job utilization statistics
- **Email Outreach**: Automated user notification system for underutilized resources
- **Date Filtering**: Robust fallback logic for historical data analysis

### Command Line Tools
- **GPU Metrics**: Wait times, efficiency analysis, PI group reports
- **CPU Metrics**: Resource utilization by user and group
- **Email Generation**: Automated outreach for underutilized jobs
- **Data Export**: Convert DuckDB to CSV format

### Key Improvements
- ✅ **Fallback Logic**: Automatically uses all available data when recent data is unavailable
- ✅ **Path Standardization**: Consistent relative paths throughout the project
- ✅ **Error Handling**: Robust error handling with user-friendly messages
- ✅ **Modular Structure**: Clean separation of concerns following data science best practices

## Original Documentation

You'll need to first install a few dependencies, which include DuckDB, Pandas, and some plotting libraries.
The example here uses ```venv```, but feel free to use ```conda``` or the package manager of your choice.

    python -m venv duckdb && source duckdb/bin/activate
    pip install -r requirements.txt
    python gpu_metrics.py waittime 

This will print some statistics about queue wait times for jobs requesting various GPUs. The ```gpu_metrics.py```
and ```cpu_metrics.py``` files contain utilities for accessing the database, as well as a lot of plotting code.
Examples of the plotting routines are provided in the ```SlurmGPU.ipynb``` Jupyter notebook. 

### Jupyter notebooks

You can run Jupyter notebooks on Unity through the OpenOnDemand portal. To make your environment 
visible in Jupyter, run 

    python -m ipykernel install --user --name "Duck DB"

from within the environment. This will add "Duck DB" as a kernel option in the dropdown.

### User data and outreach

The ```zero_gpu_usage_list.py``` script generates a list of users who have repeatedly failed
to utilize requested GPUs in their jobs, and have never sucessfully used it. It generates personalized 
email bodies with user-specific resource usage. This script will only run on Unity, for users part
of the ```pi_bpachev_umass_edu``` group. It is included as an example of the sort of tool that 
might be useful to the Unity team as a final deliverable of this project.

### Support

The Unity documentation (https://docs.unity.rc.umass.edu/) has a lot of useful
background information about Unity in particular and HPC in general. It will help explain a lot of
the terms used in the dataset schema below. For specific issues with the code in this repo or the
DuckDB dataset, feel free to reach out to Benjamin Pachev on the Unity Slack.

## The dataset

The primary dataset for this project is a DuckDB database that contains information about jobs on
Unity. It is contained under ```/modules/admin-resources/reporting/slurm_data.db``` and is updated daily.
A schema is provided below. In addition to the columns in the DuckDB file, the ```gpu_metrics.py``` script
contains tools to add a number of useful derived columns for plotting and analysis.

| Column | Type | Description |
| :---    | :--- | :------------ |
| UUID   | VARCHAR | Unique identifier | 
| JobID  | INTEGER | Slurm job ID |
| ArrayID | INTEGER | Position in job array |
| JobName |  VARCHAR | Name of job |
| IsArray |  BOOLEAN | Indicator if job is part of an array |
| Interactive |  VARCHAR | Indicator if job was interactive
| Preempted |  BOOLEAN |  Was job preempted |
| Account |  VARCHAR |  Slurm account (PI group) |
| User |  VARCHAR |  Unity user |
| Constraints |  VARCHAR[] | Job constraints |
| QOS |  VARCHAR | Job QOS |
| Status |  VARCHAR | Job status on termination |
| ExitCode |  VARCHAR | Job exit code |
| SubmitTime |  TIMESTAMP_NS |  Job submission time |
| StartTime |  TIMESTAMP_NS | Job start time
| EndTime |  TIMESTAMP_NS | Job end time |
| Elapsed |  INTEGER | Job runtime (seconds) |
| TimeLimit |  INTEGER | Job time limit (seconds) |
| Partition |  VARCHAR | Job partition |
| Nodes |  VARCHAR | Job nodes as compact string |
| NodeList |  VARCHAR[] | List of job nodes |
| CPUs |  SMALLINT | Number of CPUs |
| Memory |  INTEGER | Job allocated memory (bytes) |
| GPUs |  SMALLINT | Number of GPUs requested |
| GPUType |  VARCHAR[] | List of GPU types |
| GPUMemUsage |  FLOAT | GPU memory usage (bytes) |
| GPUComputeUsage |  FLOAT | GPU compute usage (pct) |
| CPUMemUsage |  FLOAT | GPU memory usage (bytes) |
| CPUComputeUsage |  FLOAT | CPU compute usage (pct) |

