import logging
from enum import Enum, IntEnum
from typing import Union

from langchain_aws import ChatBedrock
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.language_models import BaseChatModel

from core.aws import aws_get_service
from settings import DEBUG, TokenLimits


class TemperatureLevel(float, Enum):
    CONSERVATIVE = 0.1
    BALANCED = 0.5
    CREATIVE = 0.9


class TopKLevel(IntEnum):
    CONSERVATIVE = 10
    MODERATE = 100
    DIVERSE = 250
    VERY_DIVERSE = 500


class TopPLevel(float, Enum):
    CONSERVATIVE = 0.7
    MODERATE = 0.9
    CREATIVE = 1.0


logger = logging.getLogger(__name__)


class Models(str, Enum):
    CLAUDE_37 = "eu.anthropic.claude-3-7-sonnet-20250219-v1:0"
    CLAUDE_4 = "eu.anthropic.claude-sonnet-4-20250514-v1:0"


DEFAULT_MODEL = Models.CLAUDE_4


class SilentStreamingCallbackHandler(StreamingStdOutCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:  # type: ignore
        pass


def get_llm(
    model: Union[str, Models] = DEFAULT_MODEL,
    *,
    max_tokens: int = TokenLimits.MEDIUM,
    temperature: float = TemperatureLevel.BALANCED,
    top_k: int = TopKLevel.DIVERSE,
    top_p: float = TopPLevel.CREATIVE,
    stop_sequences: Union[str, list] = "\n\nHuman",
) -> BaseChatModel:
    callback_manager = (
        CallbackManager([StreamingStdOutCallbackHandler()])
        if DEBUG
        else CallbackManager([SilentStreamingCallbackHandler()])
    )

    model_kwargs = {
        "max_tokens": max_tokens,
        "stop_sequences": (
            [stop_sequences] if isinstance(stop_sequences, str) else stop_sequences
        ),
        "temperature": temperature,
        "top_k": top_k,
        "top_p": top_p,
    }

    llm = ChatBedrock(
        model=model,
        client=aws_get_service("bedrock-runtime"),
        model_kwargs=model_kwargs,
        callback_manager=callback_manager,
    )
    logger.info(f"Model BedrockLLM ({model}) loaded")
    return llm
