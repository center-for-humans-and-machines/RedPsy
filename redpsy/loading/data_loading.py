"""Load raw data and pre-process it for data analysis."""

# isort: skip_file

from pathlib import Path

import polars as pl


from redpsy.utils import DataConfig, validate_csv_schema
from redpsy.loading.models import RegTestPrompt, ConversationDataset

from redpsy.loading.constants import REGRESSION_TEST_DATA_PATH


def _load_json_with_config(file_path: Path) -> pl.DataFrame:
    """Load JSON file using DataConfig validation.

    Args:
        file_path (Path): Path to the JSON file
        try_parse_dates (bool, optional): Whether to attempt parsing dates. Defaults to False.

    Returns:
        pl.DataFrame: Loaded DataFrame
    """
    config = DataConfig(file_path=file_path)
    return pl.read_json(config.file_path)


def _load_csv_with_config(
    file_path: Path, try_parse_dates: bool = False
) -> pl.DataFrame:
    """Load CSV file using DataConfig validation.

    Args:
        file_path (Path): Path to the CSV file
        try_parse_dates (bool, optional): Whether to attempt parsing dates. Defaults to False.

    Returns:
        pl.DataFrame: Loaded DataFrame
    """
    config = DataConfig(file_path=file_path)
    return pl.read_csv(config.file_path, try_parse_dates=try_parse_dates)


@validate_csv_schema(RegTestPrompt)
def load_regression_test_prompts(
    file_path: Path = Path(REGRESSION_TEST_DATA_PATH),
) -> pl.DataFrame:
    """Load and preprocess regression test prompts data.

    Args:
        file_path (Path): The path to the CSV file to load.

    Returns:
        pl.DataFrame: A Polars DataFrame containing the preprocessed regression test prompts data.
    """
    return _load_csv_with_config(file_path)


@validate_csv_schema(ConversationDataset)
def load_conversation_dataset(
    file_path: Path = Path(REGRESSION_TEST_DATA_PATH),
) -> pl.DataFrame:
    """Load and preprocess conversation dataset.

    Args:
        file_path (Path): The path to the JSON file to load.

    Returns:
        pl.DataFrame: A Polars DataFrame containing the preprocessed conversation dataset.
    """
    return _load_json_with_config(file_path)
