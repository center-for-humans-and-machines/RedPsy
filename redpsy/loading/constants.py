"""Constants used in data loading."""

from pathlib import Path

from redpsy.constants import DATA_DIR

# Directories
TEST_DIR: Path = Path("tests")
FIXTURES_DIR: Path = Path("fixtures")
DATASET_DIR: Path = DATA_DIR / "dataset"

# Data paths
REGRESSION_TEST_DATA_PATH: Path = (
    DATA_DIR / "Safety_Benchmark_Mental Health -Sheet1new.csv"
)
DATASET_3_CONVERSATION_STARTERS: Path = DATA_DIR / "dataset-3-conversation-starters.csv"

# Prompt paths
REDPSY_SYSTEM_PROMPT_PATH: Path = DATA_DIR / "companion-system-prompt.txt"
PSYCHIATRIST_SYSTEM_PROMPT_PATH: Path = DATA_DIR / "psychiatrist-system-prompt.txt"
RATE_CONVERSATIONS_PROMPT_PATH: Path = DATA_DIR / "rate-conversations-prompt.txt"
