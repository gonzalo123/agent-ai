import os
from enum import IntEnum
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')

DEBUG = os.getenv('DEBUG', 'False') == 'True'
load_dotenv(dotenv_path=Path(BASE_DIR).resolve().joinpath('env', ENVIRONMENT, '.env'))

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', False)
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', False)
AWS_PROFILE_NAME = os.getenv('AWS_PROFILE_NAME', False)
AWS_REGION = os.getenv('AWS_REGION')
AWS_ASSUME_ROLE = os.getenv('AWS_ASSUME_ROLE', False)


class TokenLimits(IntEnum):
    MIN_EXTENDED = 8704
    SMALL = 9216
    SMALL_PLUS = 9728
    MEDIUM_SMALL = 10240
    MEDIUM_SMALL_PLUS = 10752
    MEDIUM_LOW = 11264
    MEDIUM_LOW_PLUS = 11776
    MEDIUM = 12288
    MEDIUM_PLUS = 12800
    MEDIUM_HIGH = 13312
    MEDIUM_HIGH_PLUS = 13824
    LARGE = 14336
    LARGE_PLUS = 14848
    EXTRA_LARGE = 15360
    MAX_EXTENDED = 15872


MAX_TOKENS = TokenLimits.SMALL
