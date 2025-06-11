# Contributing Guide

Thank you for your interest in contributing to the SLURM Job Analytics project! This guide will help you get started with development and contributions.

## 🎯 Ways to Contribute

- **Bug reports**: Found an issue? Let us know!
- **Feature requests**: Have an idea for improvement?
- **Code contributions**: Fix bugs or add new features
- **Documentation**: Improve or expand the documentation
- **Testing**: Help test new features and report issues

## 🚀 Getting Started

### Development Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ds4cg-job-analytics.git
   cd ds4cg-job-analytics
   ```

2. **Set up development environment**:
   ```bash
   python -m venv duckdb
   source duckdb/bin/activate
   pip install -r requirements.txt
   ```

3. **Install additional development tools**:
   ```bash
   pip install black flake8 pytest mkdocs mkdocs-material
   ```

4. **Verify setup**:
   ```bash
   python -c "from src.analytics.gpu_metrics import GPUMetrics; print('✅ Setup successful')"
   ```

### Project Structure Understanding

```
src/
├── analytics/          # Core analysis modules
│   ├── gpu_metrics.py  # GPU job analysis
│   ├── cpu_metrics.py  # CPU job analysis
│   └── advance_gpu_metrics.py  # Advanced metrics
├── dashboard/          # Streamlit web interface
│   └── app.py
└── outreach/          # Email outreach tools
    ├── email_outreach.py
    └── email_templates.py
```

## 📝 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

Follow our coding standards:

#### Python Code Style

- Use **Black** for code formatting:
  ```bash
  black src/ tests/
  ```

- Follow **PEP 8** guidelines
- Use **type hints** where possible:
  ```python
  def analyze_jobs(data: pd.DataFrame, days_back: int = 30) -> Dict[str, Any]:
      """Analyze job data with proper type hints."""
      pass
  ```

#### Documentation Style

- Use **docstrings** for all functions and classes:
  ```python
  def calculate_efficiency(used: float, total: float) -> float:
      """Calculate resource utilization efficiency.
      
      Args:
          used: Amount of resource used
          total: Total available resource
          
      Returns:
          Efficiency ratio between 0 and 1
          
      Raises:
          ValueError: If total is zero or negative
      """
  ```

- Update documentation when adding features
- Include examples in docstrings

### 3. Test Your Changes

#### Running Tests

```bash
# Run unit tests (if available)
python -m pytest tests/

# Test imports and basic functionality
python -c "from src.analytics.gpu_metrics import GPUMetrics; GPUMetrics()"

# Test dashboard
cd src/dashboard && streamlit run app.py
```

#### Manual Testing

Test your changes with real data:

```bash
# Test analytics modules
cd src/analytics
python gpu_metrics.py waittime
python cpu_metrics.py group_stats

# Test outreach module
cd ../outreach
python email_outreach.py --email=False
```

### 4. Update Documentation

If you're adding new features:

1. **Update API documentation**: Add docstrings to new functions
2. **Update user guides**: Add examples to relevant guide sections
3. **Test documentation build**:
   ```bash
   mkdocs serve
   ```

### 5. Commit and Push

```bash
git add .
git commit -m "feat: add new GPU efficiency metric calculation"
git push origin feature/your-feature-name
```

## 🔍 Code Review Process

### Creating a Pull Request

1. **Push your branch** to your fork
2. **Open a pull request** on GitHub
3. **Fill out the PR template** with:
   - Description of changes
   - Testing performed
   - Documentation updates

### Review Criteria

Pull requests are reviewed for:

- **Functionality**: Does it work as intended?
- **Code quality**: Is it clean, readable, and well-documented?
- **Testing**: Has it been adequately tested?
- **Documentation**: Are docs updated appropriately?
- **Compatibility**: Does it break existing functionality?

## 🎨 Specific Contribution Areas

### Analytics Module Contributions

When contributing to analytics modules:

```python
# Example: Adding a new metric
def calculate_gpu_waste_score(row: pd.Series) -> float:
    """Calculate a composite GPU waste score.
    
    This metric combines memory underutilization, compute underutilization,
    and request discrepancy into a single score.
    
    Args:
        row: DataFrame row with job data
        
    Returns:
        Waste score from 0 (no waste) to 1 (maximum waste)
    """
    memory_waste = 1 - (row['GPUMemUsage'] / (row['GPUs'] * MAX_GPU_MEMORY))
    compute_waste = 1 - (row['GPUComputeUsage'] / 100)
    
    # Weighted combination
    return 0.6 * memory_waste + 0.4 * compute_waste
```

### Dashboard Contributions

For dashboard improvements:

```python
# Example: Adding a new visualization
def create_efficiency_timeline(data: pd.DataFrame) -> None:
    """Add efficiency trends over time."""
    st.subheader("GPU Efficiency Timeline")
    
    # Group by date and calculate daily efficiency
    daily_efficiency = data.groupby(data['StartTime'].dt.date).apply(
        lambda x: (x['GPUMemUsage'].sum() / (x['GPUs'].sum() * 80e9))
    )
    
    # Create plot
    fig, ax = plt.subplots(figsize=(12, 6))
    daily_efficiency.plot(ax=ax)
    ax.set_ylabel('GPU Memory Efficiency')
    ax.set_title('Daily GPU Efficiency Trends')
    
    st.pyplot(fig)
```

### Documentation Contributions

For documentation improvements:

- **User guides**: Add practical examples and tutorials
- **API docs**: Improve docstrings and add usage examples
- **Technical notes**: Document implementation decisions
- **Getting started**: Improve onboarding experience

## 🐛 Bug Reports

### Before Reporting

1. **Check existing issues** on GitHub
2. **Try the latest version** to see if it's already fixed
3. **Gather information**:
   - Python version
   - Operating system
   - Error messages
   - Steps to reproduce

### Bug Report Template

```markdown
## Bug Description
Brief description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- Python version:
- OS:
- Package versions:

## Additional Context
Any other relevant information
```

## 💡 Feature Requests

### Before Requesting

1. **Check existing issues** for similar requests
2. **Consider the scope**: Does it fit the project goals?
3. **Think about implementation**: How might it work?

### Feature Request Template

```markdown
## Feature Description
Clear description of the requested feature

## Use Case
Why is this feature needed? What problem does it solve?

## Proposed Solution
How do you envision this working?

## Alternatives Considered
What other approaches did you consider?

## Additional Context
Any other relevant information
```

## 🔒 Security Considerations

When contributing, keep in mind:

- **Data privacy**: Don't include real user data in examples
- **Database security**: Use parameterized queries
- **Input validation**: Validate all user inputs
- **Authentication**: Consider access controls for sensitive features

## 📚 Resources

### Learning Resources

- **DuckDB Documentation**: [duckdb.org](https://duckdb.org/)
- **Streamlit Documentation**: [docs.streamlit.io](https://docs.streamlit.io/)
- **Pandas Documentation**: [pandas.pydata.org](https://pandas.pydata.org/)
- **Python Style Guide**: [PEP 8](https://peps.python.org/pep-0008/)

### Project-Specific Resources

- **Unity HPC Documentation**: [docs.unity.rc.umass.edu](https://docs.unity.rc.umass.edu/)
- **SLURM Documentation**: [slurm.schedmd.com](https://slurm.schedmd.com/)

## 🤝 Community

### Communication

- **GitHub Issues**: For bugs and feature requests
- **Unity Slack**: For cluster-specific questions
- **Code Reviews**: For technical discussions

### Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers learn and contribute
- Collaborate openly and transparently

## 📋 Release Process

### Versioning

We use semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number bumped
- [ ] Release notes written
- [ ] Tagged in Git

Thank you for contributing to the SLURM Job Analytics project! Your efforts help make HPC resources more efficient and accessible for everyone. 🚀
