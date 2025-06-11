# Dashboard Module API Reference

The dashboard module provides a Streamlit-based web interface for interactive exploration of GPU and CPU job analytics.

## Overview

The dashboard offers:

- **Real-time data visualization**: Interactive charts and metrics
- **Filtering capabilities**: Date ranges, PI groups, resource types
- **Integrated email outreach**: Generate outreach emails directly from the interface
- **Export functionality**: Download analysis results

## Main Dashboard Application

::: src.dashboard.app
    options:
      show_source: true
      show_root_heading: true
      heading_level: 3

## Usage Examples

### Running the Dashboard

```bash
# Navigate to dashboard directory
cd src/dashboard

# Start the Streamlit application
streamlit run app.py
```

The dashboard will be available at `http://localhost:8501`

### Configuration

The dashboard automatically loads data from the configured database path:

```python
# Default configuration in app.py
@st.cache_resource
def load_metrics():
    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
        db_path = os.path.join(project_root, "data/raw/slurm_data_small.db")
        return GPUMetrics(metricsfile=db_path, min_elapsed=600)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None
```

### Custom Database Path

To use a different database, modify the `load_metrics()` function:

```python
# In app.py, change the db_path:
db_path = "/path/to/your/database.db"
```

## Dashboard Features

### Main Sections

1. **GPU Analytics**
   - Wait time analysis by GPU type
   - Efficiency metrics and utilization patterns
   - PI group breakdowns

2. **CPU Analytics**
   - Resource usage by user and group
   - Historical usage trends

3. **Email Outreach**
   - Automated user flagging
   - Email content generation
   - Threshold customization

### Interactive Controls

#### Sidebar Filters

```python
# Date range selector
days_back = st.sidebar.slider("Days to analyze", 1, 365, 60)

# PI group selector
pi_groups = sorted(data['Account'].unique())
selected_pi = st.sidebar.selectbox("Select PI Group", ["All"] + list(pi_groups))
```

#### Dynamic Thresholds

```python
# Memory usage threshold
threshold = st.sidebar.slider(
    "Memory usage threshold (%)", 
    min_value=1, 
    max_value=50, 
    value=10
)

# Minimum jobs for outreach
min_jobs = st.sidebar.number_input(
    "Minimum underutilized jobs", 
    min_value=1, 
    max_value=20, 
    value=3
)
```

### Data Visualization

The dashboard uses several visualization libraries:

- **Matplotlib**: Static plots and histograms
- **Seaborn**: Statistical visualizations
- **Streamlit native**: Interactive charts and metrics

#### Example Visualizations

```python
# GPU type distribution
fig, ax = plt.subplots()
gpu_counts = filtered_data['GPUType'].value_counts()
ax.pie(gpu_counts.values, labels=gpu_counts.index, autopct='%1.1f%%')
st.pyplot(fig)

# Memory usage histogram
fig, ax = plt.subplots()
memory_gb = filtered_data['GPUMemUsage'] / (2**30)
ax.hist(memory_gb, bins=50, edgecolor='black', alpha=0.7)
ax.set_xlabel('GPU Memory Usage (GB)')
ax.set_ylabel('Number of Jobs')
st.pyplot(fig)
```

## Customization

### Adding New Sections

To add a new dashboard section:

```python
# In app.py, add to the main content area
st.write("## New Analysis Section")

# Create your analysis
new_analysis_data = perform_custom_analysis(filtered_data)

# Display results
st.dataframe(new_analysis_data)
st.plotly_chart(create_custom_plot(new_analysis_data))
```

### Custom Metrics

Add custom metrics to the sidebar:

```python
# Calculate custom metrics
total_gpu_hours = (filtered_data['Elapsed'] * filtered_data['GPUs']).sum() / 3600
avg_efficiency = filtered_data['efficiency_metric'].mean()

# Display in sidebar
st.sidebar.metric(
    label="Total GPU Hours",
    value=f"{total_gpu_hours:,.0f}",
    delta=f"{total_gpu_hours - previous_period:,.0f}"
)
```

### Theming

Customize the dashboard appearance:

```python
# Set page configuration
st.set_page_config(
    page_title="SLURM Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.metric-container {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)
```

## Performance Optimization

### Caching

The dashboard uses Streamlit's caching for performance:

```python
@st.cache_resource
def load_metrics():
    """Cache the database connection and initial data load."""
    return GPUMetrics(metricsfile=db_path, min_elapsed=600)

@st.cache_data
def filter_data(data, days_back, selected_pi):
    """Cache filtered datasets to avoid recomputation."""
    # Filtering logic here
    return filtered_data
```

### Large Dataset Handling

For large datasets:

```python
# Limit data loading
@st.cache_data
def load_sample_data(sample_size=10000):
    """Load a sample of data for faster interaction."""
    return data.sample(n=sample_size)

# Progressive loading
if st.button("Load Full Dataset"):
    data = load_full_data()
else:
    data = load_sample_data()
```

## Deployment

### Local Development

```bash
# Install dependencies
pip install streamlit

# Run dashboard
cd src/dashboard
streamlit run app.py
```

### Production Deployment

#### Using Streamlit Cloud

1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Configure secrets for database access
4. Deploy automatically

#### Using Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "src/dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Environment Variables

For production, use environment variables:

```python
import os

# Database configuration
DB_PATH = os.getenv('SLURM_DB_PATH', 'data/raw/slurm_data_small.db')
MIN_ELAPSED = int(os.getenv('MIN_ELAPSED', '600'))

# Load metrics with environment config
metrics = GPUMetrics(metricsfile=DB_PATH, min_elapsed=MIN_ELAPSED)
```

## Troubleshooting

### Common Issues

!!! warning "Memory Errors"
    For large datasets, increase available memory or implement data sampling:
    ```python
    # Sample large datasets
    if len(data) > 100000:
        data = data.sample(n=50000)
        st.warning("Displaying sample of data for performance")
    ```

!!! warning "Database Connection"
    Ensure database path is correct:
    ```python
    if not os.path.exists(db_path):
        st.error(f"Database not found at {db_path}")
        st.stop()
    ```

!!! warning "Plot Rendering"
    For slow plot rendering:
    ```python
    # Use st.empty() for dynamic updates
    plot_container = st.empty()
    with plot_container.container():
        st.pyplot(fig)
    ```

### Performance Tips

- Use `st.cache_data` for expensive computations
- Implement pagination for large tables
- Use `st.expander` to hide detailed sections
- Consider data aggregation for overview metrics

## Security Considerations

!!! warning "Data Access"
    - Ensure appropriate access controls for sensitive HPC data
    - Consider authentication mechanisms for production deployment
    - Implement user-based filtering if needed

!!! tip "Best Practices"
    - Validate all user inputs
    - Sanitize data before display
    - Use HTTPS in production
    - Regular security updates for dependencies
