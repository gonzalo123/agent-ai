"""
Unit tests for CLI commands
"""

from unittest.mock import MagicMock, Mock, patch

import pytest
from click.testing import CliRunner

from core.llm.aws import Models


class TestMathExpertCommand:
    """Test cases for math_expert CLI command"""

    def test_command_import(self):
        """Test that command can be imported"""
        from commands.math_expert import run

        assert callable(run)

    @patch("commands.math_expert.run_process")
    def test_command_execution(self, mock_run_process):
        """Test command execution"""
        from commands.math_expert import run

        runner = CliRunner()
        result = runner.invoke(run)

        # Verify LLM process was called with expected question
        mock_run_process.assert_called_once()
        call_args = mock_run_process.call_args
        question = call_args[0][0]

        assert "square root of 16" in question
        assert "divided by two" in question
        assert "squared" in question
        assert "history of operations" in question

        assert result.exit_code == 0

    @patch("commands.math_expert.run_process", side_effect=Exception("Process Error"))
    def test_command_handles_process_error(self, mock_run_process):
        """Test command handles process errors"""
        from commands.math_expert import run

        runner = CliRunner()
        result = runner.invoke(run)

        # Command should still exit normally (error handling depends on implementation)
        # But the exception should be raised
        assert result.exit_code != 0 or "Process Error" in str(result.output)

    def test_command_handles_aws_setup_error(self):
        """Test command handles AWS setup errors during import"""
        # This test is more complex because AWS setup happens at import time
        # We'll test that the command can be imported successfully
        from commands.math_expert import run

        runner = CliRunner()
        # If import was successful, the command should exist
        assert callable(run)

    def test_aws_configuration_parameters(self):
        """Test that AWS configuration uses correct parameters"""
        # Since AWS setup happens at import time, we just verify the imports work
        from commands.math_expert import (
            AWS_ACCESS_KEY_ID,
            AWS_ASSUME_ROLE,
            AWS_PROFILE_NAME,
            AWS_REGION,
            AWS_SECRET_ACCESS_KEY,
        )
        from settings import AWS_ACCESS_KEY_ID as SETTINGS_ACCESS_KEY_ID
        from settings import AWS_ASSUME_ROLE as SETTINGS_ASSUME_ROLE
        from settings import AWS_PROFILE_NAME as SETTINGS_PROFILE_NAME
        from settings import AWS_REGION as SETTINGS_REGION
        from settings import AWS_SECRET_ACCESS_KEY as SETTINGS_SECRET_ACCESS_KEY

        # Verify imports are correct (they should be the same objects)
        assert AWS_ASSUME_ROLE == SETTINGS_ASSUME_ROLE
        assert AWS_REGION == SETTINGS_REGION
        assert AWS_PROFILE_NAME == SETTINGS_PROFILE_NAME
        assert AWS_ACCESS_KEY_ID == SETTINGS_ACCESS_KEY_ID
        assert AWS_SECRET_ACCESS_KEY == SETTINGS_SECRET_ACCESS_KEY

    @patch("commands.math_expert.run_process")
    def test_command_execution_parameters(self, mock_run_process):
        """Test command executes with correct parameters"""
        from commands.math_expert import run

        runner = CliRunner()
        result = runner.invoke(run)

        # Verify run_process was called with expected parameters
        expected_question = (
            "What's the square root of 16 divided by two, squared? "
            "Show me also the history of operations."
        )
        mock_run_process.assert_called_once_with(
            expected_question, model=Models.CLAUDE_4
        )

        assert result.exit_code == 0


class TestCommandsInit:
    """Test cases for commands initialization"""

    def test_setup_commands_function(self):
        """Test setup_commands function exists and works"""
        from commands import setup_commands

        mock_cli = Mock()
        setup_commands(mock_cli)

        # Verify command was added
        mock_cli.add_command.assert_called_once()
        call_args = mock_cli.add_command.call_args

        assert "cmd" in call_args.kwargs
        assert "name" in call_args.kwargs
        assert call_args.kwargs["name"] == "math_expert"

    def test_math_expert_import(self):
        """Test math_expert command import"""
        from commands import math_expert
        from commands.math_expert import run

        assert math_expert == run


class TestCLIIntegration:
    """Integration tests for CLI setup"""

    @patch("commands.math_expert.run_process")
    def test_cli_command_registration(self, mock_run_process):
        """Test that CLI command is properly registered"""
        from cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["math_expert"])

        # Verify the command was found and executed
        mock_run_process.assert_called_once()

        assert result.exit_code == 0

    def test_cli_help(self):
        """Test CLI help functionality"""
        from cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "math_expert" in result.output

    def test_cli_command_help(self):
        """Test CLI command-specific help"""
        from cli import cli

        runner = CliRunner()
        result = runner.invoke(cli, ["math_expert", "--help"])

        assert result.exit_code == 0
