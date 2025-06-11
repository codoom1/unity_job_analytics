# Quick Start Guide

Get up and running with the SLURM Job Analytics project in minutes!

## 🎯 What You'll Learn

- How to launch the interactive dashboard
- Basic command-line operations
- Understanding the data and outputs

## 🚀 Launch the Dashboard

The fastest way to explore the data is through our interactive dashboard:

```bash
cd src/dashboard
streamlit run app.py
```

!!! success "Dashboard Ready!"
    Open your browser to `http://localhost:8501` to access the dashboard.

### Dashboard Features

The dashboard provides several key views:

=== "GPU Analytics"
    - **Wait Time Analysis**: See queue times by GPU type
    - **Efficiency Metrics**: Identify underutilized resources
    - **PI Group Reports**: Usage breakdown by research group

=== "CPU Analytics"  
    - **Resource Usage**: CPU utilization by user and group
    - **Efficiency Trends**: Historical usage patterns

=== "Email Outreach"
    - **User Flagging**: Identify users with consistently underutilized jobs
    - **Email Generation**: Create personalized outreach content

## 📊 Explore Sample Data

Let's run some basic analytics to understand your data:

### GPU Wait Times

```bash
cd src/analytics
python gpu_metrics.py waittime
```

This shows queue wait statistics by GPU type:
```
GPU Wait Time Statistics (last 90 days):
╒═══════════════╤═══════════════╤═══════════════╤═══════════════╕
│ GPU Type      │ Median (hrs)  │ Mean (hrs)    │ Jobs Count    │
╞═══════════════╪═══════════════╪═══════════════╪═══════════════╡
│ A100-80GB     │ 2.3          │ 5.1          │ 1,234        │
│ V100-32GB     │ 1.8          │ 3.9          │ 567          │
│ RTX-6000      │ 0.9          │ 2.1          │ 890          │
╘═══════════════╧═══════════════╧═══════════════╧═══════════════╛
```

### CPU Group Statistics

```bash
python cpu_metrics.py group_stats
```

Shows CPU hours used by PI group:
```
CPU Usage by PI Group (last 6 months):
╒═══════════════════╤═══════════════╤═══════════════╕
│ PI Group          │ CPU Hours     │ % of Total    │
╞═══════════════════╪═══════════════╪═══════════════╡
│ pi_smith_lab      │ 45,678       │ 23.4%        │
│ pi_johnson_group  │ 34,567       │ 17.8%        │
│ pi_davis_team     │ 28,901       │ 14.9%        │
╘═══════════════════╧═══════════════╧═══════════════╛
```

## 🎯 Generate a PI Report

Get detailed analytics for a specific research group:

```bash
# Replace 'pi_your_group' with an actual PI group name
python gpu_metrics.py pi_report --account=pi_your_group
```

This generates:
- Job efficiency breakdown
- Memory utilization patterns
- Wait time analysis
- Resource usage recommendations

## 📧 Identify Underutilized Resources

Run the email outreach tool to find users who might benefit from optimization:

```bash
cd ../outreach
python email_outreach.py
```

Example output:
```
🎯 Email Outreach Analysis
📅 Analyzing last 60 days of data
📊 Criteria: ≥3 jobs, ≥4.0 GB wasted, <10% memory usage
================================================================================

📊 SUMMARY OF FLAGGED USERS:
• 5 users meet outreach criteria
• Total wasted GPU memory: 45.7 GB
• Total underutilized jobs: 23

👤 Top Users for Outreach:
1. user123: 8 jobs, 12.3 GB wasted
2. researcher456: 6 jobs, 9.8 GB wasted
3. student789: 5 jobs, 7.2 GB wasted
```

## 📓 Explore Jupyter Notebooks

For advanced analysis, open the included Jupyter notebook:

```bash
jupyter notebook notebooks/SlurmGPU.ipynb
```

The notebook includes:
- Interactive data exploration
- Advanced visualization examples
- Custom analysis templates

## 🔍 Understanding the Output

### Key Metrics Explained

!!! info "GPU Memory Utilization"
    - **High utilization (>70%)**: Good resource usage
    - **Medium utilization (30-70%)**: May benefit from optimization
    - **Low utilization (<30%)**: Consider smaller GPU or code optimization

!!! info "Queue Wait Times"
    - **Short waits (<1 hour)**: Resource availability is good
    - **Medium waits (1-6 hours)**: Consider alternative times or resources
    - **Long waits (>6 hours)**: High demand resource - plan accordingly

!!! info "Job Efficiency"
    - Measures how well requested resources were actually used
    - Low efficiency suggests over-requesting resources

## 🎯 Common Use Cases

### As a Researcher
- Check your group's resource usage: `gpu_metrics.py pi_report --account=your_pi`
- Find optimal GPU types for your workloads
- Identify peak usage times to avoid queues

### As a System Administrator
- Monitor overall cluster efficiency
- Generate reports for resource planning
- Identify users who might benefit from training

### As a Data Scientist
- Analyze usage patterns and trends
- Create custom visualizations
- Export data for external analysis

## 🔄 Next Steps

Now that you're familiar with the basics:

1. **[Dashboard Guide](../user-guide/dashboard.md)** - Master all dashboard features
2. **[Command Line Tools](../user-guide/command-line-tools.md)** - Learn advanced CLI usage
3. **[API Reference](../api-reference/analytics.md)** - Understand the code structure

## 💡 Tips for Success

!!! tip "Start Small"
    Begin with your own PI group's data before analyzing the entire cluster.

!!! tip "Regular Monitoring"
    Set up weekly reports to track resource usage trends.

!!! tip "Share Insights"
    Use the dashboard to show utilization patterns to your research group.

## 🆘 Need Help?

If you encounter issues:

1. Check the [Installation Guide](installation.md) for setup problems
2. Review error messages carefully - they often contain helpful hints
3. Use the `--help` flag with command-line tools for usage information
4. Reach out on Unity Slack for cluster-specific questions
