"""Base command class for creating CLI commands with common functionality."""

import abc
import logging
from typing import Any, Dict, Optional

import click

from core.aws import setup_aws_conf
from settings import (
    AWS_ACCESS_KEY_ID,
    AWS_ASSUME_ROLE,
    AWS_PROFILE_NAME,
    AWS_REGION,
    AWS_SECRET_ACCESS_KEY,
)


class BaseCommand(abc.ABC):
    """Abstract base class for CLI commands with common functionality."""
    
    def __init__(self, setup_aws: bool = True) -> None:
        """Initialize the base command.
        
        Args:
            setup_aws: Whether to automatically setup AWS configuration
        """
        self.logger = logging.getLogger(self.__class__.__module__)
        
        if setup_aws:
            self.setup_aws_configuration()
    
    def setup_aws_configuration(self) -> None:
        """Setup AWS configuration from environment variables."""
        setup_aws_conf(
            assume_role=AWS_ASSUME_ROLE,
            region=AWS_REGION,
            profile_name=AWS_PROFILE_NAME,
            access_key_id=AWS_ACCESS_KEY_ID,
            secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self.logger.info("AWS configuration setup completed")
    
    @abc.abstractmethod
    def execute(self, **kwargs: Any) -> None:
        """Execute the command with the given arguments.
        
        Args:
            **kwargs: Command arguments
        """
        pass
    
    def handle_error(self, error: Exception) -> None:
        """Handle command execution errors.
        
        Args:
            error: The exception that occurred
        """
        self.logger.error(f"Command execution failed: {error}")
        click.echo(f"Error: {error}", err=True)
        raise click.ClickException(str(error))


def command_decorator(
    name: Optional[str] = None,
    help: Optional[str] = None,
    setup_aws: bool = True,
    **click_kwargs: Any
) -> Any:
    """Decorator to create CLI commands with common functionality.
    
    Args:
        name: Command name (defaults to function name)
        help: Command help text
        setup_aws: Whether to setup AWS configuration
        **click_kwargs: Additional Click command arguments
        
    Returns:
        Decorated command function
    """
    def decorator(func: Any) -> Any:
        # Setup AWS if requested
        if setup_aws:
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    setup_aws_conf(
                        assume_role=AWS_ASSUME_ROLE,
                        region=AWS_REGION,
                        profile_name=AWS_PROFILE_NAME,
                        access_key_id=AWS_ACCESS_KEY_ID,
                        secret_access_key=AWS_SECRET_ACCESS_KEY,
                    )
                    return func(*args, **kwargs)
                except Exception as e:
                    logger = logging.getLogger(func.__module__)
                    logger.error(f"Command execution failed: {e}")
                    raise click.ClickException(str(e))
            
            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
            return click.command(name=name, help=help, **click_kwargs)(wrapper)
        else:
            return click.command(name=name, help=help, **click_kwargs)(func)
    
    return decorator
