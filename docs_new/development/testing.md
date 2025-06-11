# Testing

This guide covers the testing framework and practices used in the SLURM Job Analytics project. We use a combination of unit tests, integration tests, and end-to-end tests to ensure code quality and reliability.

## Testing Framework

The project uses `pytest` as the primary testing framework, along with several additional testing utilities:

- **pytest**: Main testing framework
- **pytest-cov**: Code coverage reporting
- **pytest-mock**: Mocking and patching utilities
- **unittest.mock**: Standard library mocking
- **pandas.testing**: DataFrame comparison utilities

## Test Structure

Tests are organized in the `tests/` directory with the following structure:

```
tests/
├── conftest.py                 # Shared fixtures and configuration
├── test_analytics/            # Analytics module tests
│   ├── test_job_analyzer.py
│   ├── test_efficiency_calculator.py
│   └── test_report_generator.py
├── test_dashboard/            # Dashboard tests
│   ├── test_app.py
│   ├── test_components.py
│   └── test_data_handlers.py
├── test_outreach/            # Outreach module tests
│   ├── test_email_manager.py
│   ├── test_campaign_manager.py
│   └── test_report_generator.py
├── test_integration/         # Integration tests
│   ├── test_database_integration.py
│   ├── test_api_endpoints.py
│   └── test_workflow_integration.py
└── test_data/               # Test data and fixtures
    ├── sample_jobs.csv
    ├── test_database.db
    └── mock_responses/
```

## Running Tests

### Basic Test Execution

Run all tests:
```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v
```

Run tests for a specific module:
```bash
pytest tests/test_analytics/
```

Run a specific test file:
```bash
pytest tests/test_analytics/test_job_analyzer.py
```

Run a specific test function:
```bash
pytest tests/test_analytics/test_job_analyzer.py::test_calculate_efficiency
```

### Coverage Reporting

Run tests with coverage:
```bash
pytest --cov=src
```

Generate HTML coverage report:
```bash
pytest --cov=src --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html
```

## Writing Tests

### Unit Tests

Unit tests focus on testing individual functions and methods in isolation:

```python
# tests/test_analytics/test_efficiency_calculator.py
import pytest
from src.analytics.efficiency_calculator import EfficiencyCalculator

class TestEfficiencyCalculator:
    def setup_method(self):
        """Set up test fixtures for each test method."""
        self.calculator = EfficiencyCalculator()
    
    def test_calculate_gpu_efficiency_perfect_usage(self):
        """Test GPU efficiency calculation with 100% usage."""
        # Arrange
        gpu_time_used = 3600  # 1 hour
        gpu_time_allocated = 3600  # 1 hour
        
        # Act
        efficiency = self.calculator.calculate_gpu_efficiency(
            gpu_time_used, gpu_time_allocated
        )
        
        # Assert
        assert efficiency == 1.0
    
    def test_calculate_gpu_efficiency_zero_allocation(self):
        """Test GPU efficiency calculation with zero allocation."""
        # Arrange
        gpu_time_used = 0
        gpu_time_allocated = 0
        
        # Act & Assert
        with pytest.raises(ValueError, match="GPU time allocated cannot be zero"):
            self.calculator.calculate_gpu_efficiency(
                gpu_time_used, gpu_time_allocated
            )
    
    @pytest.mark.parametrize("used,allocated,expected", [
        (1800, 3600, 0.5),    # 50% efficiency
        (0, 3600, 0.0),       # 0% efficiency
        (3600, 7200, 0.5),    # 50% efficiency with larger numbers
    ])
    def test_calculate_gpu_efficiency_various_inputs(self, used, allocated, expected):
        """Test GPU efficiency calculation with various input combinations."""
        efficiency = self.calculator.calculate_gpu_efficiency(used, allocated)
        assert efficiency == expected
```

### Integration Tests

Integration tests verify that different components work together correctly:

```python
# tests/test_integration/test_database_integration.py
import pytest
import pandas as pd
from src.analytics.job_analyzer import JobAnalyzer
from src.database.connection import DatabaseConnection

class TestDatabaseIntegration:
    @pytest.fixture
    def db_connection(self):
        """Create a test database connection."""
        conn = DatabaseConnection(":memory:")  # In-memory database for testing
        conn.create_tables()
        return conn
    
    @pytest.fixture
    def sample_jobs_data(self, db_connection):
        """Insert sample job data for testing."""
        sample_data = pd.DataFrame({
            'job_id': [1, 2, 3],
            'user': ['alice', 'bob', 'charlie'],
            'gpu_time_used': [1800, 3600, 0],
            'gpu_time_allocated': [3600, 3600, 3600],
            'cpu_time_used': [3000, 3500, 3600],
            'cpu_time_allocated': [3600, 3600, 3600],
        })
        db_connection.insert_jobs(sample_data)
        return sample_data
    
    def test_job_analyzer_with_database(self, db_connection, sample_jobs_data):
        """Test JobAnalyzer with real database integration."""
        # Arrange
        analyzer = JobAnalyzer(db_connection)
        
        # Act
        efficiency_report = analyzer.generate_efficiency_report(
            start_date='2024-01-01',
            end_date='2024-01-31'
        )
        
        # Assert
        assert len(efficiency_report) == 3
        assert 'gpu_efficiency' in efficiency_report.columns
        assert 'cpu_efficiency' in efficiency_report.columns
        assert efficiency_report['gpu_efficiency'].iloc[0] == 0.5  # alice: 1800/3600
```

### Mocking External Dependencies

Use mocking to isolate code under test from external dependencies:

```python
# tests/test_outreach/test_email_manager.py
import pytest
from unittest.mock import Mock, patch
from src.outreach.email_manager import EmailManager

class TestEmailManager:
    def setup_method(self):
        """Set up test fixtures."""
        self.email_manager = EmailManager(
            smtp_server="test.smtp.com",
            smtp_port=587,
            sender_email="test@example.com",
            sender_password="password"
        )
    
    @patch('smtplib.SMTP')
    def test_send_email_success(self, mock_smtp):
        """Test successful email sending."""
        # Arrange
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Act
        result = self.email_manager.send_email(
            recipient="user@example.com",
            subject="Test Subject",
            body="Test Body"
        )
        
        # Assert
        assert result['success'] is True
        mock_server.send_message.assert_called_once()
    
    @patch('smtplib.SMTP')
    def test_send_email_smtp_error(self, mock_smtp):
        """Test email sending with SMTP error."""
        # Arrange
        mock_smtp.side_effect = Exception("SMTP connection failed")
        
        # Act
        result = self.email_manager.send_email(
            recipient="user@example.com",
            subject="Test Subject",
            body="Test Body"
        )
        
        # Assert
        assert result['success'] is False
        assert "SMTP connection failed" in result['error']
```

## Test Fixtures and Utilities

### Shared Fixtures

Define reusable fixtures in `conftest.py`:

```python
# tests/conftest.py
import pytest
import pandas as pd
import tempfile
import os
from src.database.connection import DatabaseConnection

@pytest.fixture
def temp_database():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    conn = DatabaseConnection(db_path)
    conn.create_tables()
    
    yield conn
    
    # Cleanup
    conn.close()
    os.unlink(db_path)

@pytest.fixture
def sample_job_data():
    """Provide sample job data for testing."""
    return pd.DataFrame({
        'job_id': range(1, 101),
        'user': [f'user{i%10}' for i in range(100)],
        'gpu_time_used': [3600 * (i % 5) / 5 for i in range(100)],
        'gpu_time_allocated': [3600] * 100,
        'cpu_time_used': [3600 * (i % 8) / 8 for i in range(100)],
        'cpu_time_allocated': [3600] * 100,
        'submit_time': pd.date_range('2024-01-01', periods=100, freq='D'),
    })

@pytest.fixture
def mock_email_config():
    """Provide mock email configuration for testing."""
    return {
        'smtp_server': 'test.smtp.com',
        'smtp_port': 587,
        'sender_email': 'test@example.com',
        'sender_password': 'test_password'
    }
```

### Custom Test Utilities

Create utility functions for common test operations:

```python
# tests/utils.py
import pandas as pd
import numpy as np

def assert_dataframes_equal(df1, df2, check_dtype=True, check_index=True):
    """
    Assert that two DataFrames are equal with better error messages.
    """
    try:
        pd.testing.assert_frame_equal(
            df1, df2, 
            check_dtype=check_dtype, 
            check_index=check_index
        )
    except AssertionError as e:
        print(f"DataFrames are not equal:\n{e}")
        print(f"First DataFrame:\n{df1}")
        print(f"Second DataFrame:\n{df2}")
        raise

def create_mock_job_data(num_jobs=10, efficiency_range=(0.1, 1.0)):
    """
    Create mock job data with controlled efficiency distribution.
    """
    np.random.seed(42)  # For reproducible tests
    
    return pd.DataFrame({
        'job_id': range(1, num_jobs + 1),
        'user': [f'user{i%5}' for i in range(num_jobs)],
        'gpu_efficiency': np.random.uniform(*efficiency_range, num_jobs),
        'cpu_efficiency': np.random.uniform(*efficiency_range, num_jobs),
        'runtime_hours': np.random.uniform(1, 24, num_jobs),
    })
```

## Testing Best Practices

### Test Organization

1. **Group related tests**: Use classes to group related test methods
2. **Descriptive names**: Use clear, descriptive test method names
3. **One assertion per test**: Focus each test on a single behavior
4. **Arrange-Act-Assert**: Structure tests with clear sections

### Test Data Management

1. **Use fixtures**: Create reusable test data with pytest fixtures
2. **Isolate tests**: Ensure tests don't depend on external data
3. **Clean up**: Always clean up resources (databases, files) after tests
4. **Seed random data**: Use fixed seeds for reproducible random test data

### Mocking Guidelines

1. **Mock external dependencies**: Don't rely on external services in tests
2. **Mock at the right level**: Mock at the boundary of your system
3. **Verify interactions**: Assert that mocked methods are called correctly
4. **Keep mocks simple**: Avoid complex mock setups that are hard to understand

### Performance Testing

```python
# tests/test_performance.py
import pytest
import time
from src.analytics.job_analyzer import JobAnalyzer

class TestPerformance:
    @pytest.mark.performance
    def test_large_dataset_processing_time(self, large_dataset):
        """Test that large dataset processing completes within time limit."""
        analyzer = JobAnalyzer()
        
        start_time = time.time()
        result = analyzer.process_jobs(large_dataset)
        processing_time = time.time() - start_time
        
        # Should process 10,000 jobs in under 5 seconds
        assert processing_time < 5.0
        assert len(result) == len(large_dataset)
```

## Continuous Integration

### GitHub Actions

Example workflow for running tests in CI:

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml --cov-report=term
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### Test Configuration

Configure pytest with `pytest.ini`:

```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --strict-config
    --tb=short
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    performance: marks tests as performance tests
    unit: marks tests as unit tests
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

## Debugging Tests

### Running Tests in Debug Mode

Use pytest's debugging features:

```bash
# Drop into debugger on first failure
pytest --pdb

# Drop into debugger on all failures
pytest --pdb --pdbcls=IPython.terminal.debugger:TerminalPdb

# Run with more verbose output
pytest -vvv -s
```

### Using Debugging Tools

```python
# Add breakpoints in test code
def test_complex_calculation():
    result = complex_function()
    
    # Drop into debugger to inspect result
    import pdb; pdb.set_trace()
    
    assert result == expected_value
```

## Test Coverage Goals

Maintain high test coverage across the codebase:

- **Overall coverage**: Aim for >90% line coverage
- **Critical paths**: 100% coverage for critical business logic
- **New code**: All new features must include tests
- **Bug fixes**: Add regression tests for fixed bugs

Check current coverage:
```bash
pytest --cov=src --cov-report=term-missing
```

## Contributing Test Guidelines

When contributing to the project:

1. **Write tests first**: Use TDD when possible
2. **Test edge cases**: Include boundary conditions and error cases
3. **Update existing tests**: Modify tests when changing functionality
4. **Document test purpose**: Add clear docstrings to test methods
5. **Run full test suite**: Ensure all tests pass before submitting PR

For more information on contributing, see the [Contributing Guide](contributing.md).
