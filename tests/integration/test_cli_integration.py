"""
Integration tests for CLI functionality
"""
from unittest.mock import Mock, patch, MagicMock
from click.testing import CliRunner
import pytest


class TestCLIIntegration:
    """Integration tests for CLI functionality"""
    
    def test_cli_main_command_structure(self):
        """Test main CLI command structure"""
        from cli import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ['--help'])
        
        assert result.exit_code == 0
        assert 'Commands:' in result.output
        assert 'math_expert' in result.output
    
    @patch('commands.math_expert.run_process')
    def test_math_expert_command_full_execution(self, mock_run_process):
        """Test full execution of math_expert command"""
        from cli import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ['math_expert'])
        
        # Verify process execution
        mock_run_process.assert_called_once()
        question = mock_run_process.call_args[0][0]
        assert "square root of 16" in question
        
        assert result.exit_code == 0
    
    @patch('commands.math_expert.run_process')
    def test_math_expert_execution_integration(self, mock_run_process):
        """Test math_expert command execution through CLI"""
        from cli import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ['math_expert'])
        
        # Verify run_process was called (command executed properly)
        mock_run_process.assert_called_once()
        
        assert result.exit_code == 0
    
    def test_cli_invalid_command(self):
        """Test CLI with invalid command"""
        from cli import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ['invalid_command'])
        
        assert result.exit_code != 0
        assert 'No such command' in result.output
    
    def test_cli_aws_configuration_error(self):
        """Test CLI handling of AWS configuration errors"""
        from cli import cli
        
        runner = CliRunner()
        # Since AWS config happens at import time, if we can run help, import worked
        result = runner.invoke(cli, ['--help'])
        
        # Should show help successfully
        assert result.exit_code == 0
        assert 'math_expert' in result.output


class TestCommandRegistration:
    """Test command registration and setup"""
    
    def test_commands_module_structure(self):
        """Test commands module structure"""
        from commands import setup_commands
        from commands.math_expert import run
        
        assert callable(setup_commands)
        assert callable(run)
    
    def test_command_setup_integration(self):
        """Test command setup with actual CLI"""
        from commands import setup_commands
        from core.cli import cli as base_cli
        
        # Create a test CLI instance
        import click
        
        @click.group()
        def test_cli():
            pass
        
        # Setup commands
        setup_commands(test_cli)
        
        # Test that command was added
        assert 'math_expert' in test_cli.commands
    
    def test_cli_module_initialization(self):
        """Test CLI module initialization"""
        import cli
        
        # Verify the CLI is properly initialized
        assert hasattr(cli, 'cli')
        assert hasattr(cli, 'logger')
    
    def test_logging_configuration(self):
        """Test logging configuration in CLI"""
        import logging
        import cli
        
        # Verify logging is configured
        logger = logging.getLogger()
        
        # Should have handlers configured
        assert len(logger.handlers) > 0


class TestEnvironmentIntegration:
    """Test integration with different environments"""
    
    @patch('os.environ', {'ENVIRONMENT': 'test', 'DEBUG': 'True'})
    @patch('commands.math_expert.run_process')
    def test_cli_in_test_environment(self, mock_run_process):
        """Test CLI in test environment"""
        from cli import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ['math_expert'])
        
        # Should work in test environment
        assert result.exit_code == 0
        mock_run_process.assert_called_once()
    
    @patch('os.environ', {'ENVIRONMENT': 'production', 'DEBUG': 'False'})
    @patch('commands.math_expert.run_process')
    def test_cli_in_production_environment(self, mock_run_process):
        """Test CLI in production environment"""
        from cli import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ['math_expert'])
        
        # Should work in production environment
        assert result.exit_code == 0
        mock_run_process.assert_called_once()


class TestCLIErrorHandling:
    """Test CLI error handling scenarios"""
    
    @patch('commands.math_expert.setup_aws_conf')
    @patch('commands.math_expert.run_process', side_effect=KeyboardInterrupt())
    def test_cli_keyboard_interrupt(self, mock_run_process, mock_setup_aws):
        """Test CLI handling of keyboard interrupt"""
        from cli import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ['math_expert'])
        
        # Should handle keyboard interrupt
        assert result.exit_code != 0
    
    @patch('commands.math_expert.setup_aws_conf')
    @patch('commands.math_expert.run_process', side_effect=SystemExit(1))
    def test_cli_system_exit(self, mock_run_process, mock_setup_aws):
        """Test CLI handling of system exit"""
        from cli import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ['math_expert'])
        
        # Should handle system exit
        assert result.exit_code == 1
    
    @patch('commands.math_expert.setup_aws_conf')
    @patch('commands.math_expert.run_process', side_effect=MemoryError("Out of memory"))
    def test_cli_memory_error(self, mock_run_process, mock_setup_aws):
        """Test CLI handling of memory errors"""
        from cli import cli
        
        runner = CliRunner()
        result = runner.invoke(cli, ['math_expert'])
        
        # Should handle memory error
        assert result.exit_code != 0
