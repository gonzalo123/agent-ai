"""
Mock utilities for testing
"""

import json
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, Mock, patch


class MockMathTools:
    """Mock implementation of MathTools for testing"""

    def __init__(self):
        self.history = []

    def _diff_values(self, a: int, b: int) -> int:
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result

    def _sum_values(self, a: int, b: int) -> int:
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def _get_history(self) -> str:
        if not self.history:
            return "No previous operations"
        return "\n".join(self.history[-5:])

    def get_tools(self):
        """Return mock tools for testing"""
        tools = []

        diff_tool = Mock()
        diff_tool.name = "diff_values"
        diff_tool.description = "Calculates the difference between two numbers"
        diff_tool.func = self._diff_values
        tools.append(diff_tool)

        sum_tool = Mock()
        sum_tool.name = "sum_values"
        sum_tool.description = "Sums two numbers"
        sum_tool.func = self._sum_values
        tools.append(sum_tool)

        history_tool = Mock()
        history_tool.name = "get_history"
        history_tool.description = "Gets the operation history"
        history_tool.func = self._get_history
        tools.append(history_tool)

        return tools


class MockBedrockClient:
    """Mock Bedrock client for testing"""

    def __init__(self, responses: Optional[Dict[str, Any]] = None):
        self.responses = responses or {}
        self.call_count = 0

    def invoke_model(self, **kwargs) -> Dict[str, Any]:
        """Mock invoke_model method"""
        self.call_count += 1

        # Return predefined response if available
        model_id = kwargs.get("modelId", "default")
        if model_id in self.responses:
            return self.responses[model_id]

        # Default response
        return {
            "body": Mock(
                read=Mock(
                    return_value=json.dumps(
                        {"completion": "Mock response", "stop_reason": "end_turn"}
                    ).encode()
                )
            ),
            "contentType": "application/json",
            "ResponseMetadata": {"HTTPStatusCode": 200, "RequestId": "mock-request-id"},
        }


class MockChatBedrock:
    """Mock ChatBedrock for testing"""

    def __init__(self, model: str = None, client: Any = None, **kwargs):
        self.model = model
        self.client = client
        self.model_kwargs = kwargs.get("model_kwargs", {})
        self.callback_manager = kwargs.get("callback_manager")
        self.call_count = 0
        self.responses = []

    def invoke(self, input_data: Any) -> Mock:
        """Mock invoke method"""
        self.call_count += 1

        # Create mock response
        response = Mock()
        response.content = f"Mock LLM response for: {input_data}"

        return response

    def set_responses(self, responses: List[str]):
        """Set predefined responses for testing"""
        self.responses = responses

    def get_response(self, index: int = 0) -> str:
        """Get response by index"""
        if index < len(self.responses):
            return self.responses[index]
        return "Default mock response"


class MockAgentExecutor:
    """Mock AgentExecutor for testing"""

    def __init__(self, agent: Any = None, tools: List = None, **kwargs):
        self.agent = agent
        self.tools = tools or []
        self.verbose = kwargs.get("verbose", False)
        self.max_iterations = kwargs.get("max_iterations", 15)
        self.early_stopping_method = kwargs.get("early_stopping_method", "generate")
        self.call_count = 0
        self.responses = {}

    def invoke(self, input_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Mock invoke method"""
        self.call_count += 1
        input_text = input_dict.get("input", "")

        # Return predefined response if available
        if input_text in self.responses:
            return self.responses[input_text]

        # Generate default response based on input
        if "history" in input_text.lower():
            output = "Mock history response"
        elif "+" in input_text:
            output = f"Mock addition response for: {input_text}"
        elif "-" in input_text:
            output = f"Mock subtraction response for: {input_text}"
        else:
            output = f"Mock response for: {input_text}"

        return {"input": input_text, "output": output, "intermediate_steps": []}

    def set_response(self, input_text: str, response: Dict[str, Any]):
        """Set a predefined response for specific input"""
        self.responses[input_text] = response


class MockAWSSession:
    """Mock AWS Session for testing"""

    def __init__(self, **kwargs):
        self.profile_name = kwargs.get("profile_name")
        self.region_name = kwargs.get("region_name")
        self.aws_access_key_id = kwargs.get("aws_access_key_id")
        self.aws_secret_access_key = kwargs.get("aws_secret_access_key")
        self.aws_session_token = kwargs.get("aws_session_token")
        self.clients = {}

    def client(self, service_name: str) -> Mock:
        """Mock client method"""
        if service_name not in self.clients:
            if service_name == "bedrock-runtime":
                self.clients[service_name] = MockBedrockClient()
            elif service_name == "sts":
                mock_sts = Mock()
                mock_sts.assume_role.return_value = {
                    "Credentials": {
                        "AccessKeyId": "mock-access-key",
                        "SecretAccessKey": "mock-secret-key",
                        "SessionToken": "mock-session-token",
                    }
                }
                self.clients[service_name] = mock_sts
            else:
                self.clients[service_name] = Mock()

        return self.clients[service_name]


class MockPromptTemplate:
    """Mock prompt template for testing"""

    def __init__(self, messages: List = None):
        self.messages = messages or []

    @classmethod
    def from_messages(cls, messages: List):
        """Mock from_messages class method"""
        return cls(messages)

    def format(self, **kwargs) -> str:
        """Mock format method"""
        return f"Formatted prompt with: {kwargs}"


def create_mock_environment(env_vars: Dict[str, str]):
    """Create mock environment context manager"""
    return patch.dict("os.environ", env_vars)


def create_mock_aws_services(services: Dict[str, Any]):
    """Create mock AWS services"""
    mocks = {}
    for service_name, service_mock in services.items():
        mocks[f"boto3.client.{service_name}"] = service_mock
    return mocks


def create_comprehensive_mock_setup():
    """Create a comprehensive mock setup for testing"""
    return {
        "math_tools": MockMathTools(),
        "bedrock_client": MockBedrockClient(),
        "chat_bedrock": MockChatBedrock(),
        "agent_executor": MockAgentExecutor(),
        "aws_session": MockAWSSession(),
        "prompt_template": MockPromptTemplate(),
    }


class TestContextManager:
    """Context manager for test setup and teardown"""

    def __init__(self, mocks: Dict[str, Any] = None):
        self.mocks = mocks or {}
        self.patches = []

    def __enter__(self):
        # Apply patches
        for patch_target, mock_obj in self.mocks.items():
            patcher = patch(patch_target, return_value=mock_obj)
            self.patches.append(patcher)
            patcher.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Stop all patches
        for patcher in self.patches:
            patcher.stop()
        self.patches.clear()


def mock_llm_chain(**kwargs):
    """Mock LLM chain for testing"""
    mock_chain = Mock()
    mock_chain.invoke.return_value = kwargs.get("response", "Mock chain response")
    return mock_chain


def mock_tool_execution(tool_name: str, inputs: Dict[str, Any], expected_output: Any):
    """Mock tool execution for testing"""
    mock_tool = Mock()
    mock_tool.name = tool_name
    mock_tool.func.return_value = expected_output
    mock_tool.inputs = inputs
    return mock_tool
