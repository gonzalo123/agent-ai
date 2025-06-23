"""
Unit tests for the core LLM AWS module
"""
from unittest.mock import Mock, patch, MagicMock
import pytest

from settings import TokenLimits


class TestCoreLLMAWS:
    """Test cases for core LLM AWS functionality"""
    
    def test_temperature_level_enum(self):
        """Test TemperatureLevel enum values"""
        from core.llm.aws import TemperatureLevel
        
        assert TemperatureLevel.CONSERVATIVE == 0.1
        assert TemperatureLevel.BALANCED == 0.5
        assert TemperatureLevel.CREATIVE == 0.9
    
    def test_top_k_level_enum(self):
        """Test TopKLevel enum values"""
        from core.llm.aws import TopKLevel
        
        assert TopKLevel.CONSERVATIVE == 10
        assert TopKLevel.MODERATE == 100
        assert TopKLevel.DIVERSE == 250
        assert TopKLevel.VERY_DIVERSE == 500
    
    def test_top_p_level_enum(self):
        """Test TopPLevel enum values"""
        from core.llm.aws import TopPLevel
        
        assert TopPLevel.CONSERVATIVE == 0.7
        assert TopPLevel.MODERATE == 0.9
        assert TopPLevel.CREATIVE == 1.0
    
    def test_models_enum(self):
        """Test Models enum values"""
        from core.llm.aws import Models
        
        assert Models.CLAUDE_37 == 'eu.anthropic.claude-3-7-sonnet-20250219-v1:0'
        assert Models.CLAUDE_4 == 'eu.anthropic.claude-sonnet-4-20250514-v1:0'
    
    def test_default_model(self):
        """Test default model setting"""
        from core.llm.aws import DEFAULT_MODEL, Models
        
        assert DEFAULT_MODEL == Models.CLAUDE_4
    
    def test_silent_streaming_callback_handler(self):
        """Test SilentStreamingCallbackHandler"""
        from core.llm.aws import SilentStreamingCallbackHandler
        
        handler = SilentStreamingCallbackHandler()
        # Should not raise any exception and do nothing
        handler.on_llm_new_token("test token")
    
    @patch('core.llm.aws.aws_get_service')
    @patch('core.llm.aws.ChatBedrock')
    @patch('core.llm.aws.CallbackManager')
    def test_get_llm_default_parameters(self, mock_callback_manager, mock_chat_bedrock, mock_aws_service):
        """Test get_llm with default parameters"""
        from core.llm.aws import get_llm, Models
        
        mock_client = Mock()
        mock_aws_service.return_value = mock_client
        
        mock_llm_instance = Mock()
        mock_chat_bedrock.return_value = mock_llm_instance
        
        mock_callback_instance = Mock()
        mock_callback_manager.return_value = mock_callback_instance
        
        result = get_llm()
        
        # Verify aws service call
        mock_aws_service.assert_called_once_with('bedrock-runtime')
        
        # Verify ChatBedrock initialization
        mock_chat_bedrock.assert_called_once()
        call_args = mock_chat_bedrock.call_args
        
        assert call_args.kwargs['model'] == Models.CLAUDE_4
        assert call_args.kwargs['client'] == mock_client
        assert 'model_kwargs' in call_args.kwargs
        assert call_args.kwargs['callback_manager'] == mock_callback_instance
        
        # Verify model_kwargs
        model_kwargs = call_args.kwargs['model_kwargs']
        assert model_kwargs['max_tokens'] == TokenLimits.MEDIUM  # Updated to use TokenLimits enum
        assert model_kwargs['temperature'] == 0.5  # TemperatureLevel.BALANCED
        assert model_kwargs['top_k'] == 250  # TopKLevel.DIVERSE
        assert model_kwargs['top_p'] == 1.0  # TopPLevel.CREATIVE
        assert model_kwargs['stop_sequences'] == ["\n\nHuman"]
        
        assert result == mock_llm_instance
    
    @patch('core.llm.aws.aws_get_service')
    @patch('core.llm.aws.ChatBedrock')
    @patch('core.llm.aws.CallbackManager')
    def test_get_llm_custom_parameters(self, mock_callback_manager, mock_chat_bedrock, mock_aws_service):
        """Test get_llm with custom parameters"""
        from core.llm.aws import get_llm, Models, TemperatureLevel, TopKLevel, TopPLevel
        
        mock_client = Mock()
        mock_aws_service.return_value = mock_client
        
        mock_llm_instance = Mock()
        mock_chat_bedrock.return_value = mock_llm_instance
        
        mock_callback_instance = Mock()
        mock_callback_manager.return_value = mock_callback_instance
        
        result = get_llm(
            model=Models.CLAUDE_37,
            max_tokens=2048,
            temperature=TemperatureLevel.CREATIVE,
            top_k=TopKLevel.CONSERVATIVE,
            top_p=TopPLevel.CONSERVATIVE,
            stop_sequences=["STOP", "END"]
        )
        
        # Verify ChatBedrock initialization with custom parameters
        call_args = mock_chat_bedrock.call_args
        
        assert call_args.kwargs['model'] == Models.CLAUDE_37
        
        model_kwargs = call_args.kwargs['model_kwargs']
        assert model_kwargs['max_tokens'] == 2048
        assert model_kwargs['temperature'] == TemperatureLevel.CREATIVE
        assert model_kwargs['top_k'] == TopKLevel.CONSERVATIVE
        assert model_kwargs['top_p'] == TopPLevel.CONSERVATIVE
        assert model_kwargs['stop_sequences'] == ["STOP", "END"]
        
        assert result == mock_llm_instance
    
    @patch('core.llm.aws.aws_get_service')
    @patch('core.llm.aws.ChatBedrock')
    @patch('core.llm.aws.CallbackManager')
    @patch('core.llm.aws.DEBUG', True)
    def test_get_llm_debug_mode(self, mock_callback_manager, mock_chat_bedrock, mock_aws_service):
        """Test get_llm in debug mode"""
        from core.llm.aws import get_llm, StreamingStdOutCallbackHandler
        
        mock_client = Mock()
        mock_aws_service.return_value = mock_client
        
        mock_llm_instance = Mock()
        mock_chat_bedrock.return_value = mock_llm_instance
        
        mock_callback_instance = Mock()
        mock_callback_manager.return_value = mock_callback_instance
        
        with patch('core.llm.aws.StreamingStdOutCallbackHandler') as mock_streaming_handler:
            mock_handler_instance = Mock()
            mock_streaming_handler.return_value = mock_handler_instance
            
            result = get_llm()
            
            # Verify that streaming handler is used in debug mode
            mock_callback_manager.assert_called_once_with([mock_handler_instance])
    
    @patch('core.llm.aws.aws_get_service')
    @patch('core.llm.aws.ChatBedrock')
    @patch('core.llm.aws.CallbackManager')
    @patch('core.llm.aws.DEBUG', False)
    def test_get_llm_production_mode(self, mock_callback_manager, mock_chat_bedrock, mock_aws_service):
        """Test get_llm in production mode (non-debug)"""
        from core.llm.aws import get_llm, SilentStreamingCallbackHandler
        
        mock_client = Mock()
        mock_aws_service.return_value = mock_client
        
        mock_llm_instance = Mock()
        mock_chat_bedrock.return_value = mock_llm_instance
        
        mock_callback_instance = Mock()
        mock_callback_manager.return_value = mock_callback_instance
        
        with patch('core.llm.aws.SilentStreamingCallbackHandler') as mock_silent_handler:
            mock_handler_instance = Mock()
            mock_silent_handler.return_value = mock_handler_instance
            
            result = get_llm()
            
            # Verify that silent handler is used in production mode
            mock_callback_manager.assert_called_once_with([mock_handler_instance])
    
    @patch('core.llm.aws.aws_get_service')
    @patch('core.llm.aws.ChatBedrock')
    def test_get_llm_string_stop_sequence(self, mock_chat_bedrock, mock_aws_service):
        """Test get_llm with string stop sequence"""
        from core.llm.aws import get_llm
        
        mock_client = Mock()
        mock_aws_service.return_value = mock_client
        
        mock_llm_instance = Mock()
        mock_chat_bedrock.return_value = mock_llm_instance
        
        result = get_llm(stop_sequences="STOP")
        
        call_args = mock_chat_bedrock.call_args
        model_kwargs = call_args.kwargs['model_kwargs']
        
        # String should be converted to list
        assert model_kwargs['stop_sequences'] == ["STOP"]
    
    @patch('core.llm.aws.aws_get_service')
    @patch('core.llm.aws.ChatBedrock')
    def test_get_llm_list_stop_sequences(self, mock_chat_bedrock, mock_aws_service):
        """Test get_llm with list stop sequences"""
        from core.llm.aws import get_llm
        
        mock_client = Mock()
        mock_aws_service.return_value = mock_client
        
        mock_llm_instance = Mock()
        mock_chat_bedrock.return_value = mock_llm_instance
        
        stop_sequences = ["STOP", "END", "FINISH"]
        result = get_llm(stop_sequences=stop_sequences)
        
        call_args = mock_chat_bedrock.call_args
        model_kwargs = call_args.kwargs['model_kwargs']
        
        # List should remain as list
        assert model_kwargs['stop_sequences'] == stop_sequences
    
    @patch('core.llm.aws.aws_get_service', side_effect=Exception("AWS Error"))
    def test_get_llm_handles_aws_error(self, mock_aws_service):
        """Test get_llm handles AWS service errors"""
        from core.llm.aws import get_llm
        
        with pytest.raises(Exception, match="AWS Error"):
            get_llm()
    
    @patch('core.llm.aws.aws_get_service')
    @patch('core.llm.aws.ChatBedrock', side_effect=Exception("Bedrock Error"))
    def test_get_llm_handles_bedrock_error(self, mock_chat_bedrock, mock_aws_service):
        """Test get_llm handles Bedrock initialization errors"""
        from core.llm.aws import get_llm
        
        mock_client = Mock()
        mock_aws_service.return_value = mock_client
        
        with pytest.raises(Exception, match="Bedrock Error"):
            get_llm()
