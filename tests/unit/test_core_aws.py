"""
Unit tests for the core AWS module
"""
from unittest.mock import Mock, patch, MagicMock
import boto3
import pytest


class TestCoreAWS:
    """Test cases for core AWS functionality"""
    
    def test_conf_initialization(self):
        """Test Conf model initialization"""
        from core.aws import Conf
        
        conf = Conf()
        assert conf.AWS_ASSUME_ROLE is False
        assert conf.AWS_REGION is None
        assert conf.AWS_PROFILE_NAME is None
        assert conf.AWS_ACCESS_KEY_ID is None
        assert conf.AWS_SECRET_ACCESS_KEY is None
        assert conf.session is None
    
    def test_get_aws_conf_with_parameters(self):
        """Test get_aws_conf function with parameters"""
        from core.aws import get_aws_conf
        
        conf = get_aws_conf(
            assume_role="test-role",
            region="us-west-2",
            profile_name="test-profile",
            access_key_id="test-key",
            secret_access_key="test-secret"
        )
        
        assert conf.AWS_ASSUME_ROLE == "test-role"
        assert conf.AWS_REGION == "us-west-2"
        assert conf.AWS_PROFILE_NAME == "test-profile"
        assert conf.AWS_ACCESS_KEY_ID == "test-key"
        assert conf.AWS_SECRET_ACCESS_KEY == "test-secret"
    
    def test_get_aws_conf_partial_parameters(self):
        """Test get_aws_conf with only some parameters"""
        from core.aws import get_aws_conf
        
        conf = get_aws_conf(region="eu-central-1", profile_name="my-profile")
        
        assert conf.AWS_REGION == "eu-central-1"
        assert conf.AWS_PROFILE_NAME == "my-profile"
        assert conf.AWS_ASSUME_ROLE is False  # Default value
        assert conf.AWS_ACCESS_KEY_ID is None  # Not set
    
    def test_setup_aws_conf_modifies_global_conf(self):
        """Test that setup_aws_conf modifies the global configuration"""
        from core.aws import setup_aws_conf, conf
        
        original_region = conf.AWS_REGION
        
        setup_aws_conf(region="test-region", profile_name="test-profile")
        
        assert conf.AWS_REGION == "test-region"
        assert conf.AWS_PROFILE_NAME == "test-profile"
        
        # Cleanup
        conf.AWS_REGION = original_region
    
    @patch('boto3.Session')
    def test_get_aws_session_with_profile(self, mock_session):
        """Test get_aws_session with profile configuration"""
        from core.aws import get_aws_session, Conf
        
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        
        aws_conf = Conf(
            AWS_PROFILE_NAME="test-profile",
            AWS_REGION="us-east-1",
            AWS_ASSUME_ROLE=False
        )
        
        result = get_aws_session(aws_conf)
        
        mock_session.assert_called_once_with(
            profile_name="test-profile",
            region_name="us-east-1"
        )
        assert result == mock_session_instance
    
    @patch('boto3.Session')
    def test_get_aws_session_with_credentials(self, mock_session):
        """Test get_aws_session with direct credentials"""
        from core.aws import get_aws_session, Conf
        
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        
        aws_conf = Conf(
            AWS_ACCESS_KEY_ID="test-key",
            AWS_SECRET_ACCESS_KEY="test-secret",
            AWS_REGION="us-east-1",
            AWS_ASSUME_ROLE=False,
            AWS_PROFILE_NAME=None
        )
        
        result = get_aws_session(aws_conf)
        
        mock_session.assert_called_once_with(
            aws_access_key_id="test-key",
            aws_secret_access_key="test-secret",
            region_name="us-east-1"
        )
        assert result == mock_session_instance
    
    @patch('boto3.client')
    @patch('boto3.Session')
    def test_get_aws_session_with_assume_role(self, mock_session, mock_client):
        """Test get_aws_session with assume role"""
        from core.aws import get_aws_session, Conf
        
        # Mock STS client for assume role
        mock_sts_client = Mock()
        mock_sts_client.assume_role.return_value = {
            'Credentials': {
                'AccessKeyId': 'assumed-key',
                'SecretAccessKey': 'assumed-secret',
                'SessionToken': 'assumed-token'
            }
        }
        mock_client.return_value = mock_sts_client
        
        # Mock final session
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        
        aws_conf = Conf(
            AWS_ACCESS_KEY_ID="root-key",
            AWS_SECRET_ACCESS_KEY="root-secret",
            AWS_REGION="us-east-1",
            AWS_ASSUME_ROLE="arn:aws:iam::123456789012:role/test-role"
        )
        
        result = get_aws_session(aws_conf)
        
        # Verify STS client creation
        mock_client.assert_called_once_with(
            'sts',
            aws_access_key_id="root-key",
            aws_secret_access_key="root-secret"
        )
        
        # Verify assume role call
        mock_sts_client.assume_role.assert_called_once_with(
            RoleArn="arn:aws:iam::123456789012:role/test-role",
            RoleSessionName='AssumeRoleSession'
        )
        
        # Verify session creation with assumed credentials
        mock_session.assert_called_once_with(
            aws_access_key_id='assumed-key',
            aws_secret_access_key='assumed-secret',
            aws_session_token='assumed-token',
            region_name='us-east-1'
        )
        
        assert result == mock_session_instance
    
    @patch('core.aws.get_aws_session')
    def test_aws_get_service(self, mock_get_session):
        """Test aws_get_service function"""
        from core.aws import aws_get_service
        
        mock_session = Mock()
        mock_client = Mock()
        mock_session.client.return_value = mock_client
        mock_get_session.return_value = mock_session
        
        result = aws_get_service('bedrock-runtime')
        
        mock_get_session.assert_called_once()
        mock_session.client.assert_called_once_with('bedrock-runtime')
        assert result == mock_client
    
    @patch('core.aws.get_aws_session')
    def test_aws_get_service_with_custom_conf(self, mock_get_session):
        """Test aws_get_service with custom configuration"""
        from core.aws import aws_get_service, Conf
        
        mock_session = Mock()
        mock_client = Mock()
        mock_session.client.return_value = mock_client
        mock_get_session.return_value = mock_session
        
        custom_conf = Conf(AWS_REGION="eu-west-1")
        result = aws_get_service('s3', aws_conf=custom_conf)
        
        mock_get_session.assert_called_once_with(custom_conf)
        mock_session.client.assert_called_once_with('s3')
        assert result == mock_client
    
    def test_conf_arbitrary_types_allowed(self):
        """Test that Conf allows arbitrary types (for boto3.Session)"""
        from core.aws import Conf
        import boto3
        
        session = boto3.Session()
        conf = Conf(session=session)
        
        assert conf.session == session
    
    def test_conf_model_validation(self):
        """Test Conf model validation"""
        from core.aws import Conf
        
        # Test valid configuration
        conf = Conf(
            AWS_ASSUME_ROLE=True,
            AWS_REGION="us-east-1",
            AWS_PROFILE_NAME="test",
            AWS_ACCESS_KEY_ID="key",
            AWS_SECRET_ACCESS_KEY="secret"
        )
        
        assert conf.AWS_ASSUME_ROLE is True
        assert conf.AWS_REGION == "us-east-1"
        assert conf.AWS_PROFILE_NAME == "test"
        assert conf.AWS_ACCESS_KEY_ID == "key"
        assert conf.AWS_SECRET_ACCESS_KEY == "secret"
