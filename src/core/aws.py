from typing import Any, Optional, Union

import boto3
from pydantic import BaseModel, ConfigDict


class Conf(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    AWS_ASSUME_ROLE: Union[bool, str] = False  # Can be boolean or ARN string
    AWS_REGION: Optional[str] = None
    AWS_PROFILE_NAME: Optional[str] = None
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    session: Optional[boto3.Session] = None


def get_aws_conf(
    assume_role: Union[bool, str, None] = None,
    region: Optional[str] = None,
    profile_name: Optional[str] = None,
    access_key_id: Optional[str] = None,
    secret_access_key: Optional[str] = None,
) -> Conf:
    """Create an AWS configuration object with the provided parameters.

    Args:
        assume_role: Boolean flag or ARN string for role assumption
        region: AWS region
        profile_name: AWS profile name
        access_key_id: AWS access key ID
        secret_access_key: AWS secret access key

    Returns:
        Configured AWS configuration object
    """
    aws_conf = Conf()
    if assume_role is not None:
        aws_conf.AWS_ASSUME_ROLE = assume_role
    if region is not None:
        aws_conf.AWS_REGION = region
    if profile_name is not None:
        aws_conf.AWS_PROFILE_NAME = profile_name
    if access_key_id is not None:
        aws_conf.AWS_ACCESS_KEY_ID = access_key_id
    if secret_access_key is not None:
        aws_conf.AWS_SECRET_ACCESS_KEY = secret_access_key
    return aws_conf


def setup_aws_conf(
    assume_role: Union[bool, str, None] = None,
    region: Optional[str] = None,
    profile_name: Optional[str] = None,
    access_key_id: Optional[str] = None,
    secret_access_key: Optional[str] = None,
) -> None:
    """Setup the global AWS configuration with the provided parameters.

    Args:
        assume_role: Boolean flag or ARN string for role assumption
        region: AWS region
        profile_name: AWS profile name
        access_key_id: AWS access key ID
        secret_access_key: AWS secret access key
    """
    if assume_role is not None:
        conf.AWS_ASSUME_ROLE = assume_role
    if region is not None:
        conf.AWS_REGION = region
    if profile_name is not None:
        conf.AWS_PROFILE_NAME = profile_name
    if access_key_id is not None:
        conf.AWS_ACCESS_KEY_ID = access_key_id
    if secret_access_key is not None:
        conf.AWS_SECRET_ACCESS_KEY = secret_access_key


def get_aws_session(aws_conf: Conf) -> boto3.Session:
    """Create a boto3 session from AWS configuration.

    Args:
        aws_conf: AWS configuration object

    Returns:
        Configured boto3 session
    """
    # AWS_ASSUME_ROLE can be either bool (False) or string (ARN)
    # If it's a string, it means we should assume the role
    if aws_conf.AWS_ASSUME_ROLE and isinstance(aws_conf.AWS_ASSUME_ROLE, str):
        session_root_account = boto3.client(
            "sts",
            aws_access_key_id=aws_conf.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=aws_conf.AWS_SECRET_ACCESS_KEY,
        )
        assume_role_response = session_root_account.assume_role(
            RoleArn=aws_conf.AWS_ASSUME_ROLE, RoleSessionName="AssumeRoleSession"
        )["Credentials"]

        session = boto3.Session(
            aws_access_key_id=assume_role_response["AccessKeyId"],
            aws_secret_access_key=assume_role_response["SecretAccessKey"],
            aws_session_token=assume_role_response["SessionToken"],
            region_name=aws_conf.AWS_REGION,
        )
    elif aws_conf.AWS_PROFILE_NAME:
        session = boto3.Session(
            profile_name=aws_conf.AWS_PROFILE_NAME, region_name=aws_conf.AWS_REGION
        )
    else:
        session = boto3.Session(
            aws_access_key_id=aws_conf.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=aws_conf.AWS_SECRET_ACCESS_KEY,
            region_name=aws_conf.AWS_REGION,
        )
    return session


conf = Conf()


def aws_get_service(service_name: str, aws_conf: Optional[Conf] = None) -> Any:
    """Get an AWS service client using the configured session.

    Args:
        service_name: Name of the AWS service (e.g., 's3', 'bedrock-runtime')
        aws_conf: Optional AWS configuration, uses global config if None

    Returns:
        AWS service client
    """
    session = get_aws_session(conf if aws_conf is None else aws_conf)
    return session.client(service_name)  # type: ignore
