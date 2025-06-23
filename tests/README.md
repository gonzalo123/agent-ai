# Test Suite Documentation

## Overview

This test suite provides comprehensive testing for the Math Expert LLM Application, covering all major components and functionality.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Pytest configuration and fixtures
├── run_tests.py               # Test runner script
├── test_performance.py        # Performance and stress tests
├── unit/                      # Unit tests for individual components
│   ├── test_settings.py       # Settings module tests
│   ├── test_tools.py          # MathTools tests
│   ├── test_prompts.py        # Prompts module tests
│   ├── test_llm.py            # LLM module tests
│   ├── test_core_aws.py       # Core AWS functionality tests
│   ├── test_core_llm_aws.py   # Core LLM AWS tests
│   └── test_commands.py       # CLI commands tests
├── integration/               # Integration tests
│   ├── test_application_integration.py  # Complete workflow tests
│   └── test_cli_integration.py         # CLI integration tests
└── fixtures/                  # Test data and utilities
    ├── test_data.py           # Sample data for tests
    └── mock_utils.py          # Mock utilities and helpers
```

## Test Categories

### Unit Tests
- **Settings Tests**: Configuration and environment variable handling
- **Tools Tests**: MathTools functionality and tool creation
- **Prompts Tests**: Prompt template validation
- **LLM Tests**: LLM module functionality
- **Core AWS Tests**: AWS configuration and session management
- **Core LLM AWS Tests**: Bedrock integration and model handling
- **Commands Tests**: CLI command functionality

### Integration Tests
- **Application Integration**: Complete workflow from input to output
- **CLI Integration**: Command-line interface integration
- **Error Handling**: Error propagation across components
- **Environment Integration**: Multi-environment testing

### Performance Tests
- **MathTools Performance**: Operation execution speed
- **History Management**: Large dataset handling
- **LLM Initialization**: Model loading performance
- **Concurrent Access**: Thread safety and parallel execution
- **Memory Usage**: Resource consumption monitoring

## Running Tests

### Prerequisites

Ensure all dependencies are installed:
```bash
poetry install --with dev
```

### Basic Usage

```bash
# Run all tests
python run_tests.py all

# Run only unit tests
python run_tests.py unit

# Run only integration tests
python run_tests.py integration

# Run performance tests
python run_tests.py performance

# Run fast tests only (exclude performance tests)
python run_tests.py fast
```

### Advanced Options

```bash
# Verbose output
python run_tests.py all -v

# Without coverage
python run_tests.py unit --no-coverage

# Parallel execution
python run_tests.py all -p

# Check dependencies
python run_tests.py --check-deps
```

### Using pytest directly

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_tools.py

# Run tests with specific marker
pytest -m unit

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test method
pytest tests/unit/test_tools.py::TestMathTools::test_sum_values_calculation
```

## Test Markers

Tests are organized using pytest markers:

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.slow`: Performance/stress tests
- `@pytest.mark.aws`: Tests requiring AWS services
- `@pytest.mark.llm`: Tests using LLM services

## Mock Strategy

The test suite uses comprehensive mocking to:

1. **Isolate Components**: Each component is tested independently
2. **Avoid External Dependencies**: No real AWS or LLM calls in tests
3. **Ensure Predictability**: Consistent test results
4. **Speed Up Execution**: Fast test execution

### Key Mock Components

- **MockMathTools**: Standalone MathTools implementation
- **MockBedrockClient**: AWS Bedrock client simulation
- **MockChatBedrock**: LLM chat interface simulation
- **MockAgentExecutor**: LangChain agent execution simulation
- **MockAWSSession**: AWS session management simulation

## Fixtures

Common test fixtures are available in `conftest.py`:

- `mock_aws_service`: Mock AWS service client
- `mock_bedrock_llm`: Mock Bedrock LLM
- `sample_math_question`: Sample questions for testing
- `sample_agent_response`: Sample agent responses
- `mock_environment_variables`: Mock environment setup
- `math_tools_instance`: Ready-to-use MathTools instance

## Coverage Requirements

The test suite maintains a minimum of 85% code coverage:

- Unit tests: Focus on individual component coverage
- Integration tests: Focus on interaction coverage
- Performance tests: Focus on edge case coverage

## Test Data

Test data is organized in `tests/fixtures/test_data.py`:

- **Sample Questions**: Common mathematical questions
- **Sample Responses**: Expected agent responses
- **Tool Configurations**: Tool setup data
- **Environment Configurations**: Different environment setups
- **Error Scenarios**: Error condition simulations

## Best Practices

### Writing New Tests

1. **Follow Naming Conventions**:
   - Test files: `test_*.py`
   - Test classes: `Test*`
   - Test methods: `test_*`

2. **Use Appropriate Markers**:
   ```python
   @pytest.mark.unit
   def test_my_function():
       pass
   ```

3. **Mock External Dependencies**:
   ```python
   @patch('module.external_dependency')
   def test_with_mock(mock_dependency):
       mock_dependency.return_value = "expected"
       # Test implementation
   ```

4. **Use Descriptive Test Names**:
   ```python
   def test_math_tools_maintains_operation_history():
       # Clear test purpose from name
   ```

5. **Follow AAA Pattern**:
   ```python
   def test_example():
       # Arrange - Set up test data
       tools = MathTools()
       
       # Act - Execute the function
       result = tools._sum_values(2, 3)
       
       # Assert - Verify the result
       assert result == 5
   ```

### Test Organization

- Group related tests in classes
- Use fixtures for common setup
- Keep tests independent and atomic
- Test both success and failure cases

### Error Testing

Always test error conditions:

```python
def test_handles_invalid_input():
    with pytest.raises(ValueError, match="Invalid input"):
        function_under_test(invalid_input)
```

## Continuous Integration

The test suite is designed to work with CI/CD systems:

- All tests should pass in isolated environments
- No external service dependencies
- Clear exit codes for automation
- Comprehensive coverage reporting

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure `src` directory is in Python path
2. **Mock Failures**: Check mock setup and patch targets
3. **Coverage Issues**: Verify all code paths are tested
4. **Performance Test Failures**: Check system resources and timing

### Debugging Tests

```bash
# Run with debugging
pytest --pdb

# Run specific test with output
pytest -s tests/unit/test_tools.py::TestMathTools::test_sum_values_calculation

# Show fixture values
pytest --fixtures
```

## Contributing

When adding new features:

1. Write tests first (TDD approach)
2. Ensure all existing tests pass
3. Add appropriate markers
4. Update documentation
5. Maintain coverage requirements

For bug fixes:
1. Write a test that reproduces the bug
2. Fix the bug
3. Ensure the test passes
4. Add regression tests if needed

## Maintenance

Regular maintenance tasks:

- Update test dependencies
- Review and update mock data
- Check for deprecated testing patterns
- Monitor test execution times
- Update documentation
