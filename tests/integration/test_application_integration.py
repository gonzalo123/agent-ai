"""
Integration tests for the complete application workflow
"""
from unittest.mock import Mock, patch, MagicMock
import pytest


class TestApplicationIntegration:
    """Integration tests for complete application workflows"""
    
    @patch('core.aws.boto3.Session')
    @patch('core.llm.aws.ChatBedrock')
    @patch('langchain.agents.AgentExecutor')
    def test_complete_math_question_workflow(self, mock_agent_executor, mock_chat_bedrock, mock_boto_session):
        """Test complete workflow from question to answer"""
        # Setup mocks
        mock_session = Mock()
        mock_boto_session.return_value = mock_session
        
        mock_client = Mock()
        mock_session.client.return_value = mock_client
        
        mock_llm = Mock()
        mock_chat_bedrock.return_value = mock_llm
        
        mock_executor = Mock()
        mock_executor.invoke.return_value = {
            "input": "What is 5 + 3?",
            "output": "The answer is 8. I used the sum_values tool to add 5 + 3 = 8.",
            "intermediate_steps": []
        }
        mock_agent_executor.return_value = mock_executor
        
        # Execute the workflow
        from modules.llm import run
        
        with patch('modules.llm.logger') as mock_logger:
            run("What is 5 + 3?")
        
        # Verify the complete chain
        mock_boto_session.assert_called()
        mock_chat_bedrock.assert_called_once()
        mock_agent_executor.assert_called_once()
        mock_executor.invoke.assert_called_once_with({"input": "What is 5 + 3?"})
        mock_logger.info.assert_called_once_with("Agent response: The answer is 8. I used the sum_values tool to add 5 + 3 = 8.")
    
    @patch('core.aws.boto3.Session')
    @patch('core.llm.aws.ChatBedrock')
    @patch('modules.llm.AgentExecutor')
    def test_complex_math_workflow_with_tools(self, mock_agent_executor, mock_chat_bedrock, mock_boto_session):
        """Test complex math workflow that uses multiple tools"""
        # Setup mocks
        mock_session = Mock()
        mock_boto_session.return_value = mock_session
        
        mock_client = Mock()
        mock_session.client.return_value = mock_client
        
        mock_llm = Mock()
        mock_chat_bedrock.return_value = mock_llm
        
        # Simulate agent using multiple tools
        mock_executor_instance = Mock()
        mock_executor_instance.invoke.return_value = {
            "input": "What is 10 - 5 + 3?",
            "output": "First I calculated 10 - 5 = 5, then 5 + 3 = 8. The final answer is 8.",
            "intermediate_steps": [
                ("diff_values", "10 - 5 = 5"),
                ("sum_values", "5 + 3 = 8")
            ]
        }
        mock_agent_executor.return_value = mock_executor_instance
        
        from modules.llm import run
        
        with patch('modules.llm.logger') as mock_logger:
            run("What is 10 - 5 + 3?")
        
        # Verify execution
        mock_executor_instance.invoke.assert_called_once_with({"input": "What is 10 - 5 + 3?"})
        mock_logger.info.assert_called_once()
    
    @patch('core.aws.setup_aws_conf')
    @patch('modules.llm.run')
    def test_cli_to_llm_integration(self, mock_llm_run, mock_setup_aws):
        """Test integration from CLI command to LLM execution"""
        from click.testing import CliRunner
        from commands.math_expert import run as cli_run
        
        runner = CliRunner()
        result = runner.invoke(cli_run)
        
        # Verify AWS setup
        mock_setup_aws.assert_called_once()
        
        # Verify LLM run was called
        mock_llm_run.assert_called_once()
        call_args = mock_llm_run.call_args
        question = call_args[0][0]
        
        # Verify the predefined question
        assert "square root of 16" in question
        
        assert result.exit_code == 0
    
    def test_math_tools_integration_with_history(self):
        """Test MathTools integration maintaining operation history"""
        from modules.tools import MathTools
        
        tools = MathTools()
        
        # Perform multiple operations
        result1 = tools._sum_values(5, 3)
        result2 = tools._diff_values(10, 4)
        result3 = tools._sum_values(result1, result2)
        
        # Verify results
        assert result1 == 8
        assert result2 == 6
        assert result3 == 14
        
        # Verify history
        history = tools._get_history()
        assert "5 + 3 = 8" in history
        assert "10 - 4 = 6" in history
        assert "8 + 6 = 14" in history
        
        # Verify history order
        lines = history.split('\n')
        assert len(lines) == 3
    
    @patch('core.aws.boto3.Session')
    def test_aws_configuration_integration(self, mock_boto_session):
        """Test AWS configuration integration"""
        from core.aws import setup_aws_conf, aws_get_service
        
        mock_session = Mock()
        mock_client = Mock()
        mock_session.client.return_value = mock_client
        mock_boto_session.return_value = mock_session
        
        # Setup AWS configuration
        setup_aws_conf(
            assume_role=False,
            region="us-east-1",
            profile_name="test-profile",
            access_key_id="test-key",
            secret_access_key="test-secret"
        )
        
        # Get service
        client = aws_get_service('bedrock-runtime')
        
        # Verify integration
        mock_boto_session.assert_called_once_with(
            profile_name="test-profile",
            region_name="us-east-1"
        )
        mock_session.client.assert_called_once_with('bedrock-runtime')
        assert client == mock_client
    
    def test_settings_environment_integration(self):
        """Test settings integration with environment variables"""
        import os
        import importlib
        import settings
        from unittest.mock import patch
        
        # Store original environment values
        original_env = {}
        for key in ['ENVIRONMENT', 'DEBUG', 'AWS_REGION', 'AWS_PROFILE_NAME']:
            original_env[key] = os.environ.get(key)
        
        test_env = {
            'ENVIRONMENT': 'test',
            'DEBUG': 'True',
            'AWS_REGION': 'eu-west-1',
            'AWS_PROFILE_NAME': 'integration-test'
        }
        
        try:
            with patch.dict(os.environ, test_env):
                # Force reload of settings
                importlib.reload(settings)
                
                assert settings.ENVIRONMENT == 'test'
                assert settings.DEBUG is True
                assert settings.AWS_REGION == 'eu-west-1'
                assert settings.AWS_PROFILE_NAME == 'integration-test'
        finally:
            # Restore original environment
            for key, value in original_env.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value
            
            # Reload settings with original environment
            importlib.reload(settings)


class TestErrorHandlingIntegration:
    """Integration tests for error handling across components"""
    
    @patch('core.aws.boto3.Session', side_effect=Exception("AWS Connection Error"))
    def test_aws_connection_error_propagation(self, mock_boto_session):
        """Test error propagation when AWS connection fails"""
        from core.aws import aws_get_service
        
        with pytest.raises(Exception, match="AWS Connection Error"):
            aws_get_service('bedrock-runtime')
    
    @patch('core.llm.aws.aws_get_service', side_effect=Exception("Bedrock Service Error"))
    def test_llm_service_error_propagation(self, mock_aws_service):
        """Test error propagation when Bedrock service fails"""
        from core.llm.aws import get_llm
        
        with pytest.raises(Exception, match="Bedrock Service Error"):
            get_llm()
    
    @patch('core.aws.get_aws_session')
    @patch('core.llm.aws.ChatBedrock')
    @patch('modules.llm.MathTools', side_effect=Exception("Tools Error"))
    def test_tools_error_propagation(self, mock_math_tools, mock_chat_bedrock, mock_aws_session):
        """Test error propagation when tools initialization fails"""
        # Mock AWS session to avoid AWS configuration errors
        mock_aws_session.return_value = Mock()
        mock_chat_bedrock.return_value = Mock()
        
        from modules.llm import run
        
        with pytest.raises(Exception, match="Tools Error"):
            run("What is 1 + 1?")


class TestPerformanceIntegration:
    """Integration tests for performance characteristics"""
    
    def test_math_tools_performance_with_large_history(self):
        """Test MathTools performance with large operation history"""
        from modules.tools import MathTools
        import time
        
        tools = MathTools()
        
        # Perform many operations
        start_time = time.time()
        for i in range(100):
            tools._sum_values(i, i + 1)
        
        # Get history (should only return last 5)
        history = tools._get_history()
        end_time = time.time()
        
        # Verify performance and correctness
        assert len(history.split('\n')) == 5  # Only last 5 operations
        assert end_time - start_time < 1.0  # Should be fast
        
        # Verify last operations are correct
        assert "99 + 100 = 199" in history
        assert "95 + 96 = 191" in history
    
    def test_prompt_template_creation_performance(self):
        """Test prompt template creation performance"""
        from langchain.prompts import ChatPromptTemplate
        from modules.prompts import AGENT_SYSTEM_PROMPT
        import time
        
        start_time = time.time()
        
        # Create multiple prompt templates (simulating multiple requests)
        for _ in range(10):
            prompt = ChatPromptTemplate.from_messages([
                ("system", AGENT_SYSTEM_PROMPT),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}")
            ])
        
        end_time = time.time()
        
        # Should be reasonably fast
        assert end_time - start_time < 1.0
        assert hasattr(prompt, 'messages')
        assert len(prompt.messages) == 3
