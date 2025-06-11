# Database Schema Reference

This document describes the structure and contents of the SLURM database used for job analytics.

## Overview

The primary dataset is a DuckDB database containing information about jobs on the Unity HPC cluster. The database is updated daily and contains comprehensive job metadata, resource usage, and performance metrics.

## Database Location

- **Production**: `/modules/admin-resources/reporting/slurm_data.db` (Unity cluster)
- **Development**: `data/raw/slurm_data_small.db` (sample dataset)

## Schema Definition

### Core Job Information

| Column | Type | Description |
|--------|------|-------------|
| `UUID` | VARCHAR | Unique identifier for the job record |
| `JobID` | INTEGER | SLURM job ID (may not be unique for array jobs) |
| `ArrayID` | INTEGER | Position in job array (NULL for non-array jobs) |
| `JobName` | VARCHAR | User-defined name of the job |
| `IsArray` | BOOLEAN | Indicator if job is part of an array |
| `Interactive` | VARCHAR | Indicator if job was interactive session |

### User and Account Information

| Column | Type | Description |
|--------|------|-------------|
| `Account` | VARCHAR | SLURM account (PI group identifier) |
| `User` | VARCHAR | Unity username |
| `QOS` | VARCHAR | Quality of Service level |

### Job Lifecycle

| Column | Type | Description |
|--------|------|-------------|
| `Status` | VARCHAR | Job status on termination |
| `ExitCode` | VARCHAR | Job exit code |
| `SubmitTime` | TIMESTAMP_NS | Job submission time |
| `StartTime` | TIMESTAMP_NS | Job start time |
| `EndTime` | TIMESTAMP_NS | Job end time |
| `Elapsed` | INTEGER | Job runtime in seconds |
| `TimeLimit` | INTEGER | Job time limit in seconds |
| `Preempted` | BOOLEAN | Was job preempted |

### Resource Allocation

| Column | Type | Description |
|--------|------|-------------|
| `Partition` | VARCHAR | SLURM partition where job ran |
| `Nodes` | VARCHAR | Job nodes as compact string |
| `NodeList` | VARCHAR[] | List of individual job nodes |
| `CPUs` | SMALLINT | Number of CPU cores allocated |
| `Memory` | INTEGER | Job allocated memory in bytes |

### GPU Resources

| Column | Type | Description |
|--------|------|-------------|
| `GPUs` | SMALLINT | Number of GPUs requested |
| `GPUType` | VARCHAR[] | List of GPU types (e.g., ['A100-80GB']) |
| `Constraints` | VARCHAR[] | Job constraints (e.g., GPU memory requirements) |

### Resource Usage Metrics

| Column | Type | Description |
|--------|------|-------------|
| `GPUMemUsage` | FLOAT | GPU memory usage in bytes |
| `GPUComputeUsage` | FLOAT | GPU compute usage as percentage |
| `CPUMemUsage` | FLOAT | CPU memory usage in bytes |
| `CPUComputeUsage` | FLOAT | CPU compute usage as percentage |

## Derived Columns

The analytics modules add several computed columns for analysis:

### GPU-Specific Derived Columns

| Column | Description | Calculation |
|--------|-------------|-------------|
| `requested_vram` | Requested GPU memory in GB | Extracted from constraints or default values |
| `gpu_hours` | Total GPU compute hours | `(Elapsed * GPUs) / 3600` |
| `memory_efficiency` | GPU memory utilization ratio | `GPUMemUsage / (GPUs * max_gpu_memory)` |
| `queued_seconds` | Time spent in queue | `StartTime - SubmitTime` |

### Advanced Metrics (from `advance_gpu_metrics.py`)

| Column | Description |
|--------|-------------|
| `gpu_utilization_efficiency` | Ratio of actual GPU compute to theoretical maximum |
| `memory_utilization_ratio` | GPU memory used vs. total available |
| `cpu_gpu_balance_score` | Ratio of CPU to GPU compute usage |
| `gpu_request_discrepancy` | Difference between requested and used GPUs |
| `composite_underutilization_score` | Combined underutilization metric |

## Data Types and Formats

### Time Formats

- **TIMESTAMP_NS**: Nanosecond precision timestamps
- **INTEGER**: Durations in seconds
- Example: `2025-01-15 14:30:00.123456789`

### Array Types

```sql
-- GPU types are stored as arrays
GPUType: ['A100-80GB', 'V100-32GB']

-- Node lists are arrays of strings  
NodeList: ['node001', 'node002', 'node003']

-- Constraints include GPU memory requirements
Constraints: ['gpu:a100:4', 'mem=80G']
```

### Memory Units

- All memory values stored in **bytes**
- Convert to GB: `value / (2^30)` 
- Convert to MB: `value / (2^20)`

## Common Queries

### Basic Job Analysis

```sql
-- Jobs in last 30 days
SELECT * FROM jobs 
WHERE StartTime >= current_timestamp - INTERVAL '30 days';

-- GPU jobs only
SELECT * FROM jobs 
WHERE GPUs > 0;

-- Jobs by PI group
SELECT Account, COUNT(*) as job_count
FROM jobs 
GROUP BY Account 
ORDER BY job_count DESC;
```

### Resource Utilization

```sql
-- Average GPU memory utilization
SELECT 
    AVG(GPUMemUsage / (GPUs * 80 * 1024^3)) as avg_gpu_memory_util
FROM jobs 
WHERE GPUs > 0 AND GPUMemUsage > 0;

-- Most common GPU types
SELECT 
    unnest(GPUType) as gpu_type,
    COUNT(*) as usage_count
FROM jobs 
WHERE GPUs > 0 
GROUP BY gpu_type 
ORDER BY usage_count DESC;
```

### Queue Time Analysis

```sql
-- Average queue times by partition
SELECT 
    Partition,
    AVG((StartTime - SubmitTime) / 1e9 / 3600) as avg_queue_hours
FROM jobs 
WHERE StartTime > SubmitTime 
GROUP BY Partition;
```

## Data Quality Considerations

### Missing Data

Some jobs may have missing metrics:

- **GPUMemUsage**: May be NULL for failed jobs
- **EndTime**: NULL for running or failed jobs
- **Resource usage**: May be 0 for very short jobs

### Data Validation

```python
# Check for data quality issues
import duckdb

conn = duckdb.connect('data/raw/slurm_data_small.db')

# Jobs with missing GPU usage data
missing_gpu_data = conn.execute("""
    SELECT COUNT(*) 
    FROM jobs 
    WHERE GPUs > 0 AND GPUMemUsage IS NULL
""").fetchone()[0]

# Jobs with negative elapsed time
invalid_elapsed = conn.execute("""
    SELECT COUNT(*) 
    FROM jobs 
    WHERE Elapsed < 0
""").fetchone()[0]
```

### Filtering Recommendations

For analysis, consider filtering:

```python
# Recommended filters for reliable analysis
filtered_jobs = """
    SELECT * FROM jobs 
    WHERE 
        Elapsed >= 600                    -- Jobs >= 10 minutes
        AND StartTime IS NOT NULL        -- Valid start time
        AND (GPUs = 0 OR GPUMemUsage IS NOT NULL)  -- Valid GPU data
        AND Status IN ('COMPLETED', 'TIMEOUT', 'CANCELLED')  -- Finished jobs
"""
```

## Database Connection Examples

### Using DuckDB Directly

```python
import duckdb

# Connect to database
conn = duckdb.connect('data/raw/slurm_data_small.db')

# Query data
df = conn.execute("SELECT * FROM jobs LIMIT 1000").df()

# Close connection
conn.close()
```

### Using Project Classes

```python
from analytics.gpu_metrics import GPUMetrics
from analytics.cpu_metrics import CPUMetrics

# Load GPU data with filtering
gpu_metrics = GPUMetrics(
    metricsfile="data/raw/slurm_data_small.db",
    min_elapsed=600  # Filter short jobs
)

# Access the data
df = gpu_metrics.df
print(f"Loaded {len(df)} GPU jobs")
```

## Performance Tips

### Indexing

For better query performance, consider creating indexes:

```sql
-- Index on commonly filtered columns
CREATE INDEX idx_start_time ON jobs(StartTime);
CREATE INDEX idx_account ON jobs(Account);
CREATE INDEX idx_gpus ON jobs(GPUs);
```

### Query Optimization

```sql
-- Use column selection to reduce memory usage
SELECT JobID, StartTime, GPUs, GPUMemUsage 
FROM jobs 
WHERE StartTime >= '2025-01-01';

-- Filter early in queries
SELECT Account, AVG(Elapsed) 
FROM jobs 
WHERE Elapsed >= 600 AND GPUs > 0  -- Filter first
GROUP BY Account;
```

## Schema Evolution

### Version History

- **v1.0**: Initial schema with basic SLURM fields
- **v1.1**: Added GPU resource tracking
- **v1.2**: Enhanced with usage metrics
- **v2.0**: Added array support and advanced metrics

### Backward Compatibility

When schema changes, older code may need updates:

```python
# Handle missing columns gracefully
def safe_column_access(df, column, default=0):
    """Safely access DataFrame column with fallback."""
    return df[column] if column in df.columns else default

# Usage
gpu_usage = safe_column_access(df, 'GPUMemUsage', 0)
```

This schema documentation should be updated whenever the database structure changes to ensure accurate analysis and proper data interpretation.
