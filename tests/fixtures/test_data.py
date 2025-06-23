"""
Test fixtures and mock data for the test suite
"""
import json
from pathlib import Path


# Sample AWS responses
SAMPLE_BEDROCK_RESPONSE = {
    "ResponseMetadata": {
        "RequestId": "12345678-1234-1234-1234-123456789012",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "content-type": "application/json",
            "content-length": "123"
        }
    },
    "contentType": "application/json",
    "body": json.dumps({
        "completion": "The answer to 5 + 3 is 8.",
        "stop_reason": "end_turn",
        "model": "claude-3-sonnet"
    }).encode()
}

# Sample mathematical questions
SAMPLE_QUESTIONS = [
    "What is 5 + 3?",
    "Calculate 15 - 7",
    "What is the result of 12 + 8 - 5?",
    "Show me the history of operations",
    "What's the square root of 2500 divided by two, squared?",
    "Calculate 25 * 4 using repeated addition",
    "What is 100 / 5 using repeated subtraction?",
    "Find the square root of 144"
]

# Sample agent responses
SAMPLE_AGENT_RESPONSES = {
    "simple_addition": {
        "input": "What is 5 + 3?",
        "output": "I'll add 5 and 3 for you. Using the sum_values tool: 5 + 3 = 8. The answer is 8.",
        "intermediate_steps": [
            ("sum_values", {"a": 5, "b": 3, "result": 8})
        ]
    },
    "simple_subtraction": {
        "input": "Calculate 15 - 7",
        "output": "I'll subtract 7 from 15. Using the diff_values tool: 15 - 7 = 8. The answer is 8.",
        "intermediate_steps": [
            ("diff_values", {"a": 15, "b": 7, "result": 8})
        ]
    },
    "complex_calculation": {
        "input": "What is the result of 12 + 8 - 5?",
        "output": "I'll solve this step by step. First: 12 + 8 = 20, then: 20 - 5 = 15. The final answer is 15.",
        "intermediate_steps": [
            ("sum_values", {"a": 12, "b": 8, "result": 20}),
            ("diff_values", {"a": 20, "b": 5, "result": 15})
        ]
    },
    "history_request": {
        "input": "Show me the history of operations",
        "output": "Here's the history of recent operations:\n12 + 8 = 20\n20 - 5 = 15",
        "intermediate_steps": [
            ("get_history", {"result": "12 + 8 = 20\n20 - 5 = 15"})
        ]
    }
}

# Sample tool configurations
SAMPLE_TOOL_CONFIGS = {
    "diff_values": {
        "name": "diff_values",
        "description": "Calculates the difference between two numbers",
        "parameters": {
            "a": {"type": "int", "description": "first number"},
            "b": {"type": "int", "description": "second number"}
        },
        "returns": {"type": "int", "description": "difference of a - b"}
    },
    "sum_values": {
        "name": "sum_values",
        "description": "Sums two numbers",
        "parameters": {
            "a": {"type": "int", "description": "first number"},
            "b": {"type": "int", "description": "second number"}
        },
        "returns": {"type": "int", "description": "sum of a + b"}
    },
    "get_history": {
        "name": "get_history",
        "description": "Gets the operation history",
        "parameters": {},
        "returns": {"type": "str", "description": "last operations"}
    }
}

# Sample environment configurations
SAMPLE_ENVIRONMENTS = {
    "test": {
        "DEBUG": "True",
        "ENVIRONMENT": "test",
        "AWS_REGION": "us-east-1",
        "AWS_PROFILE_NAME": "test-profile",
        "AWS_ACCESS_KEY_ID": "test-access-key",
        "AWS_SECRET_ACCESS_KEY": "test-secret-key",
        "AWS_ASSUME_ROLE": "False"
    },
    "development": {
        "DEBUG": "True",
        "ENVIRONMENT": "development",
        "AWS_REGION": "eu-central-1",
        "AWS_PROFILE_NAME": "dev-profile",
        "AWS_ACCESS_KEY_ID": "dev-access-key",
        "AWS_SECRET_ACCESS_KEY": "dev-secret-key",
        "AWS_ASSUME_ROLE": "arn:aws:iam::123456789012:role/dev-role"
    },
    "production": {
        "DEBUG": "False",
        "ENVIRONMENT": "production",
        "AWS_REGION": "us-west-2",
        "AWS_PROFILE_NAME": "prod-profile",
        "AWS_ACCESS_KEY_ID": "prod-access-key",
        "AWS_SECRET_ACCESS_KEY": "prod-secret-key",
        "AWS_ASSUME_ROLE": "arn:aws:iam::123456789012:role/prod-role"
    }
}

# Sample LLM configurations
SAMPLE_LLM_CONFIGS = {
    "conservative": {
        "model": "eu.anthropic.claude-3-7-sonnet-20250219-v1:0",
        "max_tokens": 2048,
        "temperature": 0.1,
        "top_k": 10,
        "top_p": 0.7
    },
    "balanced": {
        "model": "eu.anthropic.claude-sonnet-4-20250514-v1:0",
        "max_tokens": 4096,
        "temperature": 0.5,
        "top_k": 250,
        "top_p": 1.0
    },
    "creative": {
        "model": "eu.anthropic.claude-sonnet-4-20250514-v1:0",
        "max_tokens": 8192,
        "temperature": 0.9,
        "top_k": 500,
        "top_p": 1.0
    }
}

# Sample error scenarios
SAMPLE_ERROR_SCENARIOS = {
    "aws_connection_error": {
        "error_type": "ConnectionError",
        "message": "Unable to connect to AWS services",
        "code": "AWS_CONNECTION_FAILED"
    },
    "bedrock_service_error": {
        "error_type": "ServiceError",
        "message": "Bedrock service unavailable",
        "code": "BEDROCK_UNAVAILABLE"
    },
    "invalid_credentials": {
        "error_type": "AuthenticationError",
        "message": "Invalid AWS credentials",
        "code": "INVALID_CREDENTIALS"
    },
    "rate_limit_exceeded": {
        "error_type": "RateLimitError",
        "message": "API rate limit exceeded",
        "code": "RATE_LIMIT_EXCEEDED"
    },
    "model_not_found": {
        "error_type": "ModelError",
        "message": "Requested model not found",
        "code": "MODEL_NOT_FOUND"
    }
}

# Sample prompt templates
SAMPLE_PROMPT_TEMPLATES = {
    "system_prompt": """
You are an expert mathematical agent specialized in calculations.

You have access to the following tools:
- diff_values: Calculates the difference between two numbers
- sum_values: Sums two numbers
- get_history: Gets the operation history

Guidelines:
1. Only answer questions related to mathematical operations.
2. For complex operations, use step-by-step calculations.
""",
    "user_prompt": "{input}",
    "agent_scratchpad": "{agent_scratchpad}"
}

# Performance benchmarks
PERFORMANCE_BENCHMARKS = {
    "tool_execution": {
        "max_time_seconds": 0.1,
        "operations_per_second": 1000
    },
    "llm_initialization": {
        "max_time_seconds": 5.0,
        "memory_usage_mb": 100
    },
    "history_retrieval": {
        "max_time_seconds": 0.01,
        "max_operations": 10000
    }
}


def get_sample_data(data_type: str, key: str = None):
    """
    Retrieve sample data for testing
    
    Args:
        data_type: Type of data to retrieve (questions, responses, etc.)
        key: Specific key within the data type
    
    Returns:
        Sample data for testing
    """
    data_map = {
        "questions": SAMPLE_QUESTIONS,
        "responses": SAMPLE_AGENT_RESPONSES,
        "tools": SAMPLE_TOOL_CONFIGS,
        "environments": SAMPLE_ENVIRONMENTS,
        "llm_configs": SAMPLE_LLM_CONFIGS,
        "errors": SAMPLE_ERROR_SCENARIOS,
        "prompts": SAMPLE_PROMPT_TEMPLATES,
        "benchmarks": PERFORMANCE_BENCHMARKS,
        "bedrock_response": SAMPLE_BEDROCK_RESPONSE
    }
    
    if data_type not in data_map:
        raise ValueError(f"Unknown data type: {data_type}")
    
    data = data_map[data_type]
    
    if key is None:
        return data
    
    if key not in data:
        raise ValueError(f"Unknown key '{key}' for data type '{data_type}'")
    
    return data[key]


def create_mock_bedrock_response(content: str, model: str = "claude-3-sonnet") -> dict:
    """
    Create a mock Bedrock response
    
    Args:
        content: Response content
        model: Model name
    
    Returns:
        Mock Bedrock response
    """
    return {
        "ResponseMetadata": {
            "RequestId": "test-request-id",
            "HTTPStatusCode": 200
        },
        "contentType": "application/json",
        "body": json.dumps({
            "completion": content,
            "stop_reason": "end_turn",
            "model": model
        }).encode()
    }


def create_mock_agent_response(input_text: str, output_text: str, steps: list = None) -> dict:
    """
    Create a mock agent response
    
    Args:
        input_text: Input question
        output_text: Output answer
        steps: Intermediate steps
    
    Returns:
        Mock agent response
    """
    return {
        "input": input_text,
        "output": output_text,
        "intermediate_steps": steps or []
    }
