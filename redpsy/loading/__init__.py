"""Entrypoint for the loading package."""

# fmt: off
# isort: off
from redpsy.loading.constants import (
    DATA_DIR,
    REGRESSION_TEST_DATA_PATH,
    RATE_CONVERSATIONS_PROMPT_PATH,
    REDPSY_SYSTEM_PROMPT_PATH,
    PSYCHIATRIST_SYSTEM_PROMPT_PATH,
)
from redpsy.loading.data_loading import (
    load_regression_test_prompts,
)

__all__ = [
    "DATA_DIR",
    "REGRESSION_TEST_DATA_PATH",
    "RATE_CONVERSATIONS_PROMPT_PATH",
    "REDPSY_SYSTEM_PROMPT_PATH",
    "PSYCHIATRIST_SYSTEM_PROMPT_PATH",
    "load_regression_test_prompts",
]
