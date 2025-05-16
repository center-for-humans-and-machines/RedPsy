"""Rate conversation processor."""

from pathlib import Path

from redpsy.loading import RATE_CONVERSATIONS_PROMPT_PATH
from redpsy.loading.data_loading import load_conversation_dataset
from redpsy.monitoring.api import BatchConfig
from redpsy.monitoring.models import BotRatingResponse
from redpsy.monitoring.processors.base import BaseProcessor
from redpsy.utils import UTF_8, clean_text


class RateConversationsProcessor(BaseProcessor):
    """Processor for regression test data using OpenAI Batch Processing API.

    Input: JSONL file with questions
    Output: JSONL file with answers
    """

    def __init__(self, input_file: str):
        config = BatchConfig(
            system_prompt=clean_text(
                Path(RATE_CONVERSATIONS_PROMPT_PATH).read_text(encoding=UTF_8)
            ),
            input_file=input_file,
            data_loader=load_conversation_dataset,
            response_format_model=BotRatingResponse,
        )
        super().__init__(
            config,
            input_column_name="conversation",
            output_column_name="custom_rating",
        )
