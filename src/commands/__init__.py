from .math_expert import run as math_expert


def setup_commands(cli):
    cli.add_command(cmd=math_expert, name='math_expert')
