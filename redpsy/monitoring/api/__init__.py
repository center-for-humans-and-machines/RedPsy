"""Entrypoint for the API used in monitoring."""

from redpsy.monitoring.api.client import create_client
from redpsy.monitoring.api.config import BatchConfig

__all__ = ["create_client", "BatchConfig"]
