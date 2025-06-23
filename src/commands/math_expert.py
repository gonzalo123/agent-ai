import logging

import click

from core.aws import setup_aws_conf
from core.llm.aws import Models
from modules.llm import run as run_process
from settings import AWS_ASSUME_ROLE, AWS_REGION, AWS_PROFILE_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

logger = logging.getLogger(__name__)

setup_aws_conf(
    assume_role=AWS_ASSUME_ROLE,
    region=AWS_REGION,
    profile_name=AWS_PROFILE_NAME,
    access_key_id=AWS_ACCESS_KEY_ID,
    secret_access_key=AWS_SECRET_ACCESS_KEY
)


@click.command()
def run():
    question = ("What's the square root of 16 divided by two, squared? "
                "Show me also the history of operations.")
    run_process(question, model=Models.CLAUDE_4)
