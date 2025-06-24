"""
Unit tests for the LLM module
"""

from unittest.mock import MagicMock, Mock, patch

import pytest


class TestLLMModule:
    """Test cases for LLM module functionality"""

    @patch("modules.llm.get_llm")
    @patch("modules.llm.create_tool_calling_agent")
    @patch("modules.llm.AgentExecutor")
    @patch("modules.llm.MathTools")
    def test_run_function_basic_execution(
        self, mock_math_tools, mock_agent_executor, mock_create_agent, mock_get_llm
    ):
        """Test basic execution of run function"""
        # Setup mocks
        mock_tools_instance = Mock()
        mock_tools = [Mock(name="diff_values"), Mock(name="sum_values")]
        mock_tools_instance.get_tools.return_value = mock_tools
        mock_math_tools.return_value = mock_tools_instance

        mock_llm = Mock()
        mock_get_llm.return_value = mock_llm

        mock_agent = Mock()
        mock_create_agent.return_value = mock_agent

        mock_executor = Mock()
        mock_executor.invoke.return_value = {"output": "Test response"}
        mock_agent_executor.return_value = mock_executor

        # Execute
        from modules.llm import run

        with patch("modules.llm.logger") as mock_logger:
            run("What is 2 + 2?")

        # Verify
        mock_math_tools.assert_called_once()
        mock_tools_instance.get_tools.assert_called_once()
        mock_get_llm.assert_called_once()
        mock_create_agent.assert_called_once()
        mock_agent_executor.assert_called_once()
        mock_executor.invoke.assert_called_once_with({"input": "What is 2 + 2?"})
        mock_logger.info.assert_called_once_with("Agent response: Test response")

    @patch("modules.llm.get_llm")
    @patch("modules.llm.create_tool_calling_agent")
    @patch("modules.llm.AgentExecutor")
    @patch("modules.llm.MathTools")
    def test_run_function_uses_correct_model(
        self, mock_math_tools, mock_agent_executor, mock_create_agent, mock_get_llm
    ):
        """Test that run function uses correct model"""
        # Setup mocks
        mock_tools_instance = Mock()
        mock_tools_instance.get_tools.return_value = []
        mock_math_tools.return_value = mock_tools_instance

        mock_executor = Mock()
        mock_executor.invoke.return_value = {"output": "Test"}
        mock_agent_executor.return_value = mock_executor

        from core.llm.aws import Models
        from modules.llm import run

        with patch("modules.llm.logger"):
            run("test question")

        # Verify correct model is used with max_tokens parameter
        from settings import MAX_TOKENS

        mock_get_llm.assert_called_once_with(
            model=Models.CLAUDE_4, max_tokens=MAX_TOKENS
        )

    @patch("modules.llm.get_llm")
    @patch("modules.llm.create_tool_calling_agent")
    @patch("modules.llm.AgentExecutor")
    @patch("modules.llm.MathTools")
    def test_run_function_agent_executor_configuration(
        self, mock_math_tools, mock_agent_executor, mock_create_agent, mock_get_llm
    ):
        """Test AgentExecutor configuration"""
        # Setup mocks
        mock_tools_instance = Mock()
        mock_tools = [Mock()]
        mock_tools_instance.get_tools.return_value = mock_tools
        mock_math_tools.return_value = mock_tools_instance

        mock_executor = Mock()
        mock_executor.invoke.return_value = {"output": "Test"}
        mock_agent_executor.return_value = mock_executor

        from modules.llm import run

        with patch("modules.llm.logger"):
            run("test question")

        # Verify AgentExecutor configuration
        mock_agent_executor.assert_called_once()
        call_args = mock_agent_executor.call_args

        assert "agent" in call_args.kwargs
        assert "tools" in call_args.kwargs
        assert call_args.kwargs["verbose"] is True
        assert call_args.kwargs["max_iterations"] == 10
        assert call_args.kwargs["tools"] == mock_tools

    @patch("modules.llm.get_llm")
    @patch("modules.llm.create_tool_calling_agent")
    @patch("modules.llm.AgentExecutor")
    @patch("modules.llm.MathTools")
    def test_run_function_prompt_template(
        self, mock_math_tools, mock_agent_executor, mock_create_agent, mock_get_llm
    ):
        """Test prompt template creation"""
        # Setup mocks
        mock_tools_instance = Mock()
        mock_tools_instance.get_tools.return_value = []
        mock_math_tools.return_value = mock_tools_instance

        mock_executor = Mock()
        mock_executor.invoke.return_value = {"output": "Test"}
        mock_agent_executor.return_value = mock_executor

        from modules.llm import run

        with patch("modules.llm.logger"):
            run("test question")

        # Verify agent creation was called with correct parameters
        mock_create_agent.assert_called_once()
        call_args = mock_create_agent.call_args

        # Check that prompt template was passed
        assert len(call_args.args) == 3  # llm, tools, prompt
        prompt_template = call_args.args[2]

        # Verify prompt template structure
        assert hasattr(prompt_template, "messages")

    @patch("modules.llm.get_llm")
    @patch("modules.llm.create_tool_calling_agent")
    @patch("modules.llm.AgentExecutor")
    @patch("modules.llm.MathTools")
    def test_run_function_handles_complex_question(
        self, mock_math_tools, mock_agent_executor, mock_create_agent, mock_get_llm
    ):
        """Test handling of complex mathematical questions"""
        # Setup mocks
        mock_tools_instance = Mock()
        mock_tools_instance.get_tools.return_value = []
        mock_math_tools.return_value = mock_tools_instance

        mock_executor = Mock()
        mock_executor.invoke.return_value = {
            "output": "The square root of 2500 is 50, divided by 2 is 25, squared is 625."
        }
        mock_agent_executor.return_value = mock_executor

        from modules.llm import run

        complex_question = "What's the square root of 2500 divided by two, squared?"

        with patch("modules.llm.logger") as mock_logger:
            run(complex_question)

        # Verify the question was passed correctly
        mock_executor.invoke.assert_called_once_with({"input": complex_question})
        mock_logger.info.assert_called_once()

    @patch("modules.llm.get_llm")
    @patch("modules.llm.create_tool_calling_agent")
    @patch("modules.llm.AgentExecutor")
    @patch("modules.llm.MathTools")
    def test_run_function_uses_system_prompt(
        self, mock_math_tools, mock_agent_executor, mock_create_agent, mock_get_llm
    ):
        """Test that run function uses the system prompt"""
        # Setup mocks
        mock_tools_instance = Mock()
        mock_tools_instance.get_tools.return_value = []
        mock_math_tools.return_value = mock_tools_instance

        mock_executor = Mock()
        mock_executor.invoke.return_value = {"output": "Test"}
        mock_agent_executor.return_value = mock_executor

        from modules.llm import run
        from modules.prompts import AGENT_SYSTEM_PROMPT

        with patch("modules.llm.logger"):
            run("test question")

        # Verify agent creation
        mock_create_agent.assert_called_once()
        call_args = mock_create_agent.call_args

        # The prompt template should contain the system prompt
        prompt_template = call_args.args[2]
        assert hasattr(prompt_template, "messages")

    @patch("modules.llm.get_llm", side_effect=Exception("LLM Error"))
    @patch("modules.llm.MathTools")
    def test_run_function_handles_llm_error(self, mock_math_tools, mock_get_llm):
        """Test error handling when LLM fails"""
        mock_tools_instance = Mock()
        mock_tools_instance.get_tools.return_value = []
        mock_math_tools.return_value = mock_tools_instance

        from modules.llm import run

        with pytest.raises(Exception, match="LLM Error"):
            run("test question")

    @patch("modules.llm.get_llm")
    @patch("modules.llm.create_tool_calling_agent")
    @patch("modules.llm.AgentExecutor")
    @patch("modules.llm.MathTools", side_effect=Exception("Tools Error"))
    def test_run_function_handles_tools_error(
        self, mock_math_tools, mock_agent_executor, mock_create_agent, mock_get_llm
    ):
        """Test error handling when tools initialization fails"""
        from modules.llm import run

        with pytest.raises(Exception, match="Tools Error"):
            run("test question")
