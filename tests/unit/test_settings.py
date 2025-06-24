"""
Unit tests for the settings module
"""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestSettings:
    """Test cases for settings configuration"""

    def test_base_dir_path(self):
        """Test that BASE_DIR is correctly set"""
        from settings import BASE_DIR

        assert isinstance(BASE_DIR, Path)
        assert BASE_DIR.name == "src"

    def test_default_environment(self):
        """Test default environment setting"""
        with patch.dict(os.environ, {}, clear=True):
            # Reimport to get fresh settings
            import importlib

            import settings

            importlib.reload(settings)

            assert settings.ENVIRONMENT == "local"

    def test_custom_environment(self, mock_environment_variables):
        """Test custom environment setting"""
        import importlib

        import settings

        importlib.reload(settings)

        assert settings.ENVIRONMENT == "test"

    def test_debug_flag_true(self):
        """Test DEBUG flag when set to True"""
        with patch.dict(os.environ, {"DEBUG": "True"}):
            import importlib

            import settings

            importlib.reload(settings)

            assert settings.DEBUG is True

    def test_debug_flag_false(self):
        """Test DEBUG flag when set to False"""
        with patch.dict(os.environ, {"DEBUG": "False"}):
            import importlib

            import settings

            importlib.reload(settings)

            assert settings.DEBUG is False

    def test_aws_configuration(self, mock_environment_variables):
        """Test AWS configuration settings"""
        import importlib

        import settings

        importlib.reload(settings)

        assert settings.AWS_ACCESS_KEY_ID == "test_access_key"
        assert settings.AWS_SECRET_ACCESS_KEY == "test_secret_key"
        assert settings.AWS_REGION == "us-east-1"
        assert settings.AWS_PROFILE_NAME == "test_profile"

    def test_aws_assume_role_default(self):
        """Test AWS assume role default value"""
        with patch.dict(os.environ, {}, clear=True):
            import importlib

            import settings

            importlib.reload(settings)

            assert settings.AWS_ASSUME_ROLE is False

    @patch("dotenv.load_dotenv")
    def test_dotenv_loading(self, mock_load_dotenv):
        """Test that dotenv is loaded correctly"""
        import importlib

        import settings

        importlib.reload(settings)

        mock_load_dotenv.assert_called_once()
        args, kwargs = mock_load_dotenv.call_args
        assert "dotenv_path" in kwargs
        assert "local" in str(kwargs["dotenv_path"])
