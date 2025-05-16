"""Regression test processor for OpenAI Batch Processing API."""

from pathlib import Path

from redpsy.loading import (
    REDPSY_SYSTEM_PROMPT_PATH,
    REGRESSION_TEST_DATA_PATH,
    load_regression_test_prompts,
)
from redpsy.monitoring.api import BatchConfig
from redpsy.monitoring.constants import RegTestColumns
from redpsy.monitoring.processors.base import BaseProcessor
from redpsy.utils import UTF_8, clean_text


class RegTestProcessor(BaseProcessor):
    """Processor for regression test data using OpenAI Batch Processing API.

    Input: JSONL file with questions
    Output: JSONL file with answers
    """

    def __init__(self):
        config = BatchConfig(
            system_prompt=clean_text(
                Path(REDPSY_SYSTEM_PROMPT_PATH).read_text(encoding=UTF_8)
            ),
            input_file=REGRESSION_TEST_DATA_PATH,
            data_loader=load_regression_test_prompts,
        )
        super().__init__(
            config,
            input_column_name=RegTestColumns.QUESTION,
            output_column_name=RegTestColumns.ANSWER,
        )
