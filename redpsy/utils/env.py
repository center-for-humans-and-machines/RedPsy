"""Shared environment-related utilities.

Load and validate environment variables.
"""

import os

from dotenv import load_dotenv

load_dotenv()


def get_env_variable(var_name: str) -> str:
    """Get the environment variable or raise an error if not defined.

    Args:
        var_name: The name of the environment variable.

    Returns:
        str: The value of the environment variable.

    Raises:
        EnvironmentError: If the environment variable is not set.
    """
    # Ensure environment variables are loaded
    load_dotenv(override=True)

    try:
        return os.environ[var_name]
    except KeyError as e:
        raise EnvironmentError(f"Set the environment variable {var_name}") from e
