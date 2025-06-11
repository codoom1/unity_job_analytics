# Dashboard User Guide

The interactive dashboard provides a web-based interface for exploring GPU and CPU job analytics. This guide covers all dashboard features and how to use them effectively.

## 🚀 Getting Started

### Launching the Dashboard

```bash
# Navigate to the dashboard directory
cd src/dashboard

# Start the Streamlit application
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`.

### First Look

When you first open the dashboard, you'll see:

- **Main content area**: Charts and analysis results
- **Sidebar**: Filters and controls
- **Navigation**: Tabs for different analysis types

## 📊 Main Features

### Sidebar Controls

The sidebar contains all the interactive controls for filtering and customizing your analysis:

#### Date Range Filter
- **Purpose**: Analyze data from a specific time period
- **Default**: Last 60 days
- **Range**: 1 day to 1 year
- **Behavior**: Automatically falls back to all data if no recent data exists

```python
# Example: Analyze last 30 days
days_back = 30  # Set via sidebar slider
```

#### PI Group Filter
- **Purpose**: Focus analysis on specific research groups
- **Options**: "All" or select specific PI group
- **Usage**: Useful for generating group-specific reports

#### Memory Threshold
- **Purpose**: Define what constitutes "underutilized" jobs
- **Default**: 10% GPU memory usage
- **Range**: 1% to 50%
- **Impact**: Jobs below this threshold are flagged for outreach

### Main Content Sections

## 🎯 GPU Analytics Section

### GPU Usage Summary

**Location**: Main content area, top-left

**Features**:
- Total jobs analyzed
- Date range confirmation
- PI group-specific summaries when filtered

**Example Output**:
```
Analyzing 1,234 GPU jobs from last 60 days
PI Group: pi_smith_lab (234 jobs)
```

### GPU Type Distribution

**Location**: Main content area, top-right

**Chart Type**: Pie chart showing GPU usage by type

**Information Displayed**:
- Percentage of jobs by GPU type (A100-80GB, V100-32GB, etc.)
- Total job counts for each GPU type
- Visual representation of cluster GPU usage patterns

**Use Cases**:
- Identify most popular GPU types
- Plan resource allocation
- Understand demand patterns

### Memory Usage Histogram

**Location**: Main content area, middle-left

**Chart Type**: Histogram of GPU memory utilization

**Features**:
- X-axis: GPU memory usage in GB
- Y-axis: Number of jobs
- Helps identify usage patterns and outliers

**Interpretation**:
- **Peak near 0**: Many underutilized jobs
- **Multiple peaks**: Different usage patterns
- **Right-skewed**: Mix of light and heavy users

### Wait Time Analysis

**Location**: Main content area, middle-right

**Chart Type**: Box plot or bar chart of queue wait times

**Dimensions**:
- Wait times by GPU type
- Statistical measures (median, mean, quartiles)
- Helps users choose optimal GPU types

## 🖥️ CPU Analytics Section

### CPU Usage by Group

**Display**: Table format showing:
- PI group names
- Total CPU hours consumed
- Percentage of total cluster usage
- Number of jobs

**Sorting**: Automatically sorted by usage (highest first)

**Use Cases**:
- Resource accounting
- Usage planning
- Fair share analysis

### CPU Efficiency Metrics

**Display**: Charts showing:
- CPU utilization trends over time
- Efficiency by user or group
- Resource waste identification

## 📧 Email Outreach Section

### Underutilized Jobs Table

**Purpose**: Identify jobs that could benefit from optimization

**Filters Applied**:
- GPU memory usage below threshold
- Job duration minimums
- PI group filtering (if selected)

**Columns Displayed**:
- Job ID
- Username
- PI group (Account)
- GPU memory usage
- Number of GPUs requested
- Job start time

**Sorting**: Most recent jobs first

### User-Level Statistics

**Purpose**: Aggregate underutilization by user for outreach

**Metrics Calculated**:
- Number of underutilized jobs per user
- Total wasted GPU memory
- Estimated wasted GPU hours
- Last job timestamp

**Threshold Controls**:
- Minimum number of wasted jobs
- Minimum amount of wasted memory
- Configurable via sidebar

### Email Content Preview

**Feature**: Generate sample outreach emails

**Content Includes**:
- Personalized greeting
- Specific job examples with utilization data
- Optimization suggestions
- Resource links and contact information

**Use Cases**:
- System administrator outreach
- User education
- Resource optimization campaigns

## 🔧 Advanced Features

### Data Export

**CSV Download**: Export filtered data for external analysis

**Available Exports**:
- Complete job dataset (filtered)
- Underutilized jobs summary
- User-level statistics

**Usage**:
```python
# Dashboard automatically provides download buttons
# No additional configuration needed
```

### Real-Time Filtering

**Feature**: All charts update automatically when filters change

**Performance**: Utilizes Streamlit caching for smooth interaction

**Responsiveness**: Large datasets may show loading indicators

### Error Handling

**Robust Design**: Dashboard handles common issues gracefully:

- **Missing data**: Clear messages when no data matches filters
- **Database issues**: Helpful error messages for connection problems
- **Invalid inputs**: Validation prevents crashes

**Example Error Messages**:
```
⚠️ No data found in last 30 days, using all available data
❌ Database connection failed: Check file path
ℹ️ No underutilized jobs found with current criteria
```

## 📱 Mobile and Responsive Design

### Mobile Usage

**Compatibility**: Dashboard works on tablets and phones

**Recommendations**:
- Use landscape orientation for better chart viewing
- Sidebar may auto-collapse on small screens
- Touch gestures supported for chart interaction

### Browser Compatibility

**Supported Browsers**:
- Chrome (recommended)
- Firefox
- Safari
- Edge

**Requirements**:
- JavaScript enabled
- Modern browser (last 2 major versions)

## 🎨 Customization

### Themes

**Current Theme**: Material Design with blue accent

**Customization**: Modify `app.py` for different themes:

```python
st.set_page_config(
    page_title="Custom Title",
    page_icon="🔬",  # Change icon
    layout="wide"
)
```

### Adding Custom Sections

**Example**: Add a new analysis section:

```python
# In app.py, add after existing sections
st.write("## Custom Analysis")

# Your custom analysis code
custom_data = perform_custom_analysis(filtered_data)
st.dataframe(custom_data)
```

## 🔍 Troubleshooting

### Common Issues

!!! warning "Dashboard Won't Start"
    **Symptoms**: Error messages when running `streamlit run app.py`
    
    **Solutions**:
    ```bash
    # Check Python path
    export PYTHONPATH="${PYTHONPATH}:$(pwd)/../../src"
    
    # Verify dependencies
    pip install streamlit pandas matplotlib seaborn
    
    # Check database path
    ls ../../data/raw/slurm_data_small.db
    ```

!!! warning "No Data Displayed"
    **Symptoms**: Charts show empty or "No data" messages
    
    **Possible Causes**:
    - Database file missing or corrupted
    - Date filters too restrictive
    - PI group filter excluding all data
    
    **Solutions**:
    - Check database file exists and is readable
    - Expand date range or select "All" PI groups
    - Verify data exists in expected time range

!!! warning "Slow Performance"
    **Symptoms**: Dashboard takes long time to load or update
    
    **Solutions**:
    ```python
    # Reduce data size by filtering
    min_elapsed = 3600  # Only jobs > 1 hour
    
    # Use data sampling for very large datasets
    sample_size = 10000  # Limit to 10k jobs
    ```

### Performance Optimization

**For Large Datasets**:

1. **Increase minimum job duration**:
   ```python
   metrics = GPUMetrics(min_elapsed=3600)  # 1+ hour jobs
   ```

2. **Use date filtering**:
   ```python
   # Focus on recent data
   days_back = 30  # Last month only
   ```

3. **Enable Streamlit caching**:
   ```python
   @st.cache_data
   def expensive_computation(data):
       return processed_data
   ```

### Getting Help

**Resources**:
- Check the [Installation Guide](../getting-started/installation.md) for setup issues
- Review [API Documentation](../api-reference/dashboard.md) for technical details
- See [Contributing Guide](../development/contributing.md) for modification help

**Support Channels**:
- GitHub Issues for bugs
- Unity Slack for cluster-specific questions
- Project documentation for usage questions

## 💡 Tips for Effective Use

### For Researchers

1. **Start with your PI group**: Use the PI group filter to focus on your data
2. **Check queue patterns**: Use wait time analysis to plan job submissions
3. **Monitor your efficiency**: Look for your jobs in the underutilized table

### For System Administrators

1. **Regular monitoring**: Check dashboard weekly for usage patterns
2. **Outreach targeting**: Use email tools to help users optimize
3. **Resource planning**: Use GPU type distribution for capacity planning

### For Data Analysis

1. **Export for deeper analysis**: Use CSV download for external tools
2. **Time series analysis**: Vary the date range to see trends
3. **Comparative analysis**: Switch between PI groups to compare usage

The dashboard is designed to be intuitive and self-explanatory, but don't hesitate to explore all features to get the most value from your HPC job analytics!
