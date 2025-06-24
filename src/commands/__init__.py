from click import Group

from .math_expert import run as math_expert


def setup_commands(cli: Group) -> None:
    """Register all CLI commands with the main CLI group.

    Args:
        cli: The main Click CLI group to register commands with
    """
    cli.add_command(cmd=math_expert, name="math_expert")
