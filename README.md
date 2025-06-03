# Introduction

This respository is a place to contain the tools developed over the course of the DS4CG 2025 summer
internship project with Unity. It has three purposes:
1. To provide the summer internship team with some starting code and documentation of the dataset.
2. To faciliate sharing code among the team in a professional and efficient manner.
3. As the place to put the project deliverables.

## Contributing to this repository

Please feel free to use the scripts and notebook in this repository as a template for analysis efforts.
The following guidelines may prove helpful in maximizing the utility of this repository:

- Please avoid comitting code unless it is meant to be used by the rest of the team.
- New code should first be comitted in a dedicated branch (```feature/newanalysis``` or ```bugfix/typo```), and later merged into ```main``` following a code
review.
- Shared datasets should usually be managed with a shared folder on Unity, not comitted to Git.
- Prefer comitting Python modules with plotting routines like ```gpu_metrics.py``` instead of Jupyter notebooks, when possible. 
  
## Getting started on Unity

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

