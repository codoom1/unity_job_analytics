# SLURM Job Analytics Project

A comprehensive data science project for analyzing GPU and CPU job utilization on Unity HPC cluster.

## 🎯 Overview

This project provides tools and analytics for understanding resource utilization patterns on HPC clusters, specifically focusing on GPU and CPU job efficiency. It includes interactive dashboards, command-line tools, and automated outreach capabilities.

## ✨ Key Features

### 📊 Interactive Dashboard
- **Real-time Analytics**: Streamlit-based web interface for exploring job metrics
- **GPU/CPU Insights**: Comprehensive utilization statistics and visualizations
- **Date Filtering**: Robust time-based analysis with fallback logic
- **Email Integration**: Automated user notification system

### 🛠️ Command Line Tools
- **GPU Analytics**: Wait time analysis, efficiency plots, PI group reports
- **CPU Analytics**: Resource utilization by user and research group
- **Data Export**: Convert DuckDB to CSV format for external analysis
- **Email Outreach**: Automated flagging of underutilized resources

### 📈 Advanced Analytics
- **Utilization Metrics**: Memory, compute, and request discrepancy analysis
- **Pattern Recognition**: Identify inefficient resource usage patterns
- **Predictive Insights**: Queue wait time predictions and optimization suggestions

## 🚀 Quick Start

=== "Dashboard"
    ```bash
    # Start the interactive dashboard
    cd src/dashboard
    streamlit run app.py
    ```
    Access at `http://localhost:8501`

=== "Command Line"
    ```bash
    # GPU analytics
    cd src/analytics
    python gpu_metrics.py waittime
    
    # CPU analytics
    python cpu_metrics.py group_stats
    
    # Email outreach
    cd ../outreach
    python email_outreach.py --email=True
    ```

=== "Jupyter"
    ```bash
    # Launch Jupyter with the project kernel
    jupyter notebook notebooks/SlurmGPU.ipynb
    ```

## 📁 Project Structure

```
├── data/                       # Data storage
│   ├── raw/                   # Raw database files
│   └── processed/             # Processed/exported data
├── src/                       # Source code
│   ├── analytics/             # Core analytics modules
│   ├── dashboard/             # Web dashboard
│   └── outreach/              # Email outreach tools
├── notebooks/                 # Jupyter notebooks
├── scripts/                   # Utility scripts
├── docs_new/                  # Documentation (MkDocs)
└── tests/                     # Test files
```

## 🎓 For New Users

!!! tip "Getting Started"
    New to this project? Check out our [Installation Guide](getting-started/installation.md) and [Quick Start Tutorial](getting-started/quick-start.md).

!!! info "Documentation"
    Learn how to contribute to and maintain the documentation in our [Documentation Guide](getting-started/documentation-guide.md).

## 📚 Learn More

- **[User Guide](user-guide/dashboard.md)**: Detailed usage instructions
- **[API Reference](api-reference/analytics.md)**: Complete code documentation
- **[Technical Notes](technical-notes/database-schema.md)**: Implementation details
- **[Development](development/contributing.md)**: Contributing guidelines

## 🤝 Support

For questions about the codebase or database, reach out to Benjamin Pachev on the Unity Slack. For Unity HPC documentation, visit [docs.unity.rc.umass.edu](https://docs.unity.rc.umass.edu/).

---

*Built with ❤️ for the Data Science for Common Good program*
