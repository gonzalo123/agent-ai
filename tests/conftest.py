"""
Pytest configuration and fixtures for the test suite
"""

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock

import pytest

# Add src directory to Python path for imports
test_dir = Path(__file__).parent
src_dir = test_dir.parent / "src"
sys.path.insert(0, str(src_dir))


@pytest.fixture
def mock_aws_service():
    """Mock AWS service client for testing"""
    mock_client = Mock()
    mock_client.invoke_model.return_value = {
        "body": Mock(read=Mock(return_value=b'{"completion": "test response"}'))
    }
    return mock_client


@pytest.fixture
def mock_bedrock_llm():
    """Mock Bedrock LLM for testing"""
    mock_llm = Mock()
    mock_llm.invoke.return_value = Mock(content="Test LLM response")
    return mock_llm


@pytest.fixture
def sample_math_question():
    """Sample math question for testing"""
    return "What is 5 + 3?"


@pytest.fixture
def sample_agent_response():
    """Sample agent response for testing"""
    return {
        "input": "What is 5 + 3?",
        "output": "The answer to 5 + 3 is 8.",
        "intermediate_steps": [],
    }


@pytest.fixture
def mock_environment_variables():
    """Mock environment variables for testing"""
    env_vars = {
        "AWS_ACCESS_KEY_ID": "test_access_key",
        "AWS_SECRET_ACCESS_KEY": "test_secret_key",
        "AWS_REGION": "us-east-1",
        "AWS_PROFILE_NAME": "test_profile",
        "DEBUG": "True",
        "ENVIRONMENT": "test",
    }

    original_env = {}
    for key, value in env_vars.items():
        original_env[key] = os.environ.get(key)
        os.environ[key] = value

    yield env_vars

    # Restore original environment
    for key, original_value in original_env.items():
        if original_value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = original_value


@pytest.fixture
def math_tools_instance():
    """Create a MathTools instance for testing"""
    from modules.tools import MathTools

    return MathTools()


@pytest.fixture
def mock_click_context():
    """Mock Click context for CLI testing"""
    context = Mock()
    context.params = {}
    context.obj = {}
    return context


class MockAgentExecutor:
    """Mock AgentExecutor for testing"""

    def __init__(self, agent=None, tools=None, **kwargs):
        self.agent = agent
        self.tools = tools
        self.verbose = kwargs.get("verbose", False)
        self.max_iterations = kwargs.get("max_iterations", 15)

    def invoke(self, input_dict):
        return {
            "input": input_dict["input"],
            "output": f"Mock response for: {input_dict['input']}",
            "intermediate_steps": [],
        }


@pytest.fixture
def mock_agent_executor():
    """Mock AgentExecutor for testing"""
    return MockAgentExecutor
