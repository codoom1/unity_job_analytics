# Installation Guide

This guide walks you through setting up the SLURM Job Analytics project on your system.

## Prerequisites

- Python 3.8 or higher
- Access to a terminal/command line
- Git (for cloning the repository)

## Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/ds4cg-job-analytics.git
cd ds4cg-job-analytics
```

## Step 2: Set Up Virtual Environment

We recommend using a virtual environment to manage dependencies:

=== "Using venv"
    ```bash
    python -m venv duckdb
    source duckdb/bin/activate  # On Windows: duckdb\Scripts\activate
    ```

=== "Using conda"
    ```bash
    conda create -n ds4cg-analytics python=3.11
    conda activate ds4cg-analytics
    ```

## Step 3: Install Dependencies

Choose one of the following methods:

=== "Automated Setup (Recommended)"
    ```bash
    python setup.py
    ```
    This script will install all required packages with tested versions.

=== "Manual Installation"
    ```bash
    pip install -r requirements.txt
    ```

## Step 4: Verify Installation

Test that everything is working:

```bash
# Test imports
python -c "import duckdb, pandas, streamlit; print('✅ All imports successful')"

# Test database access
python -c "
import sys
sys.path.append('src')
from analytics.gpu_metrics import GPUMetrics
metrics = GPUMetrics()
print(f'✅ Loaded {len(metrics.df)} records from database')
"
```

## Step 5: Optional - Set Up Jupyter

If you plan to use the Jupyter notebooks:

```bash
python -m ipykernel install --user --name "ds4cg-analytics"
```

This adds the environment as a kernel option in Jupyter.

## Troubleshooting

### Common Issues

!!! warning "DuckDB Database Not Found"
    If you see errors about missing database files, ensure you have the sample data:
    ```bash
    ls data/raw/slurm_data_small.db
    ```

!!! warning "Module Import Errors"
    If Python can't find the project modules, check your Python path:
    ```bash
    export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
    ```

!!! warning "Permission Errors"
    On some systems, you might need to use `python3` instead of `python`:
    ```bash
    python3 -m venv duckdb
    python3 setup.py
    ```

### Fire Package Issues

If you encounter Inspector errors with the Fire package:

```bash
pip install fire==0.4.0
```

### Platform-Specific Notes

=== "macOS"
    - Ensure Xcode command line tools are installed: `xcode-select --install`
    - You might need to install Homebrew for some dependencies

=== "Linux"
    - Install system dependencies: `sudo apt-get install python3-dev`
    - Some distributions require `python3-venv` package

=== "Windows"
    - Use PowerShell or Command Prompt as Administrator
    - Replace forward slashes with backslashes in paths
    - Use `py` instead of `python` if configured

## Next Steps

Once installation is complete:

1. **[Quick Start Guide](../getting-started/quick-start.md)** - Learn basic usage
2. **[Dashboard Tutorial](../user-guide/dashboard.md)** - Explore the web interface
3. **[Command Line Tools](../user-guide/command-line-tools.md)** - Master the CLI tools

## Development Setup

If you plan to contribute to the project:

```bash
# Install development dependencies
pip install -r requirements-dev.txt  # If it exists

# Install pre-commit hooks
pre-commit install  # If using pre-commit

# Run tests
python -m pytest tests/  # If tests exist
```

See our [Contributing Guide](../development/contributing.md) for more details.
