"""Class to simulate conversation between clinician and companion using agents."""

import os
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

import pytz
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langchain_together import ChatTogether
from langfuse.callback import CallbackHandler

from redpsy.loading import (
    PSYCHIATRIST_SYSTEM_PROMPT_PATH,
    REDPSY_SYSTEM_PROMPT_PATH,
)
from redpsy.monitoring.api import BatchConfig
from redpsy.utils import UTF_8, clean_text, get_env_variable


# pylint: disable-next=too-few-public-methods
class InSilicoConversationProcessor:
    """Simulates streaming multi-turn conversations between two agents using LangChain."""

    def __init__(
        self,
        config: BatchConfig = BatchConfig(
            system_prompt=clean_text(
                Path(REDPSY_SYSTEM_PROMPT_PATH).read_text(encoding=UTF_8)
            ),
            # Dummy value to bypass validation
            input_file="data",
        ),
        tags: Optional[List[str]] = None,
        max_turns: int = 10,
    ):
        """Initialize the conversation processor with LangChain components."""
        self.max_turns = max_turns

        self.model: str = config.chat_completions_model
        self.api_version: str | None = None
        self.temperature: float = config.temperature
        self.created_at: datetime | str | None = None
        self.updated_at: datetime | str | None = None
        self.session_id = uuid.uuid4()
        # See pylint dangerous-default-value / W0102
        if tags is None:
            tags = []
        self.tags = tags
        self.print_conversation: bool = False

        model_provider: str = ""
        # Initialize LangChain chat models for both agents
        if config.is_endpoint_azure:
            self.api_version: str = get_env_variable("MODEL_API_VERSION")
            os.environ["AZURE_OPENAI_API_KEY"] = get_env_variable("MODEL_API_KEY")
            os.environ["AZURE_OPENAI_ENDPOINT"] = get_env_variable("MODEL_ENDPOINT")
            model_provider = "Azure OpenAI"
            self.companion = AzureChatOpenAI(
                azure_deployment=config.chat_completions_model,
                api_version=get_env_variable("MODEL_API_VERSION"),
                temperature=config.temperature,
            )
            self.clinician = AzureChatOpenAI(
                azure_deployment=config.chat_completions_model,
                api_version=get_env_variable("MODEL_API_VERSION"),
                temperature=config.temperature,
            )
        elif config.is_endpoint_together:
            model_provider = "Together AI"
            self.companion = ChatTogether(
                api_key=get_env_variable("MODEL_API_KEY"),
                model_name=config.chat_completions_model,
                temperature=config.temperature,
            )
            self.clinician = ChatTogether(
                api_key=get_env_variable("MODEL_API_KEY"),
                model_name=config.chat_completions_model,
                temperature=config.temperature,
            )
        elif config.is_endpoint_openai:
            model_provider = "OpenAI"
            self.companion = ChatOpenAI(
                api_key=get_env_variable("MODEL_API_KEY"),
                model_name=config.chat_completions_model,
                temperature=config.temperature,
            )
            self.clinician = ChatOpenAI(
                api_key=get_env_variable("MODEL_API_KEY"),
                model_name=config.chat_completions_model,
                temperature=config.temperature,
            )
        else:
            raise ValueError(
                "Invalid model endpoint. Please set the environment variable "
                "'MODEL_ENDPOINT' to either 'azure', 'together', or 'openai'."
            )

        self.model_provider: str = model_provider

        # Load system prompts
        self.companion_system_prompt = clean_text(
            Path(REDPSY_SYSTEM_PROMPT_PATH).read_text(encoding=UTF_8)
        )

        clinician_prompt_path = PSYCHIATRIST_SYSTEM_PROMPT_PATH
        self.clinician_system_prompt = clean_text(
            Path(clinician_prompt_path).read_text(encoding=UTF_8)
        )

        # Initialize message histories
        self.companion_messages = [SystemMessage(content=self.companion_system_prompt)]
        self.clinician_messages = [SystemMessage(content=self.clinician_system_prompt)]

    def _get_timestamp(self) -> str:
        """Get the current timestamp in ISO format."""
        return datetime.now(pytz.utc).isoformat()

    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history as a string.
        Returns:
            List[Dict]: A list of dictionaries containing the conversation history.
        """
        conversation_history = []
        turn_counter: int = 0
        # Omit the system prompt from the conversation history
        for _, message in enumerate(self.companion_messages[1:]):
            if isinstance(message, HumanMessage):
                conversation_history.append(
                    {
                        "role": "clinician",
                        "content": message.content,
                        "turn": turn_counter,
                    }
                )
            elif isinstance(message, AIMessage):
                conversation_history.append(
                    {
                        "role": "companion",
                        "content": message.content,
                        "turn": turn_counter,
                    }
                )
                turn_counter += 1
        return conversation_history

    def get_conversation_duration_in_seconds(self) -> int:
        """Get the conversation duration in seconds."""
        created_at: datetime = datetime.fromisoformat(str(self.created_at))
        updated_at: datetime = datetime.fromisoformat(str(self.updated_at))
        duration: timedelta = updated_at - created_at
        return int(duration.total_seconds())

    async def simulate_conversation(self, initial_prompt: str) -> None:
        """Simulate an async streaming conversation between the agents."""
        if self.print_conversation:
            print(f"Clinician: {initial_prompt}\n")

        langfuse_handler = CallbackHandler(
            public_key=get_env_variable("LANGFUSE_PUBLIC_KEY"),
            secret_key=get_env_variable("LANGFUSE_SECRET_KEY"),
            host=get_env_variable("LANGFUSE_HOST"),
            tags=["neurips-dataset"],
        )

        # Add initial prompt to both histories
        self.companion_messages.append(HumanMessage(content=initial_prompt))
        self.clinician_messages.append(HumanMessage(content=initial_prompt))
        self.created_at = self._get_timestamp()
        session_id = self.session_id

        for turn in range(self.max_turns):
            # companion's turn
            if self.print_conversation:
                print("Companion: ", end="", flush=True)
            companion_response = ""
            async for chunk in self.companion.astream(
                self.companion_messages,
                config={
                    # "callbacks": [langfuse_handler],
                    "tags": ["companion"] + self.tags,
                    "session": session_id,
                    "metadata": {
                        "session_id": session_id,
                        "turn": turn,
                    },
                },
            ):
                chunk_text = chunk.content
                companion_response += chunk_text
                if self.print_conversation:
                    print(chunk_text, end="", flush=True)
            if self.print_conversation:
                print("\n")

            # Update both message histories with companion's response
            self.companion_messages.append(AIMessage(content=companion_response))
            self.clinician_messages.append(HumanMessage(content=companion_response))

            # Check if this is the last turn - if so, don't get clinician response
            if turn == self.max_turns - 1:
                self.updated_at = self._get_timestamp()
                break

            # Clinician's turn
            if self.print_conversation:
                print("Clinician: ", end="", flush=True)
            clinician_response = ""
            async for chunk in self.clinician.astream(
                self.clinician_messages,
                config={
                    "callbacks": [langfuse_handler],
                    "tags": ["clinician"] + self.tags,
                    "session": session_id,
                    "metadata": {
                        "session_id": session_id,
                        "turn": turn,
                    },
                },
            ):
                chunk_text = chunk.content
                clinician_response += chunk_text
                if self.print_conversation:
                    print(chunk_text, end="", flush=True)
            if self.print_conversation:
                print("\n")

            # Update both message histories with Clinician's response
            self.companion_messages.append(HumanMessage(content=clinician_response))
            self.clinician_messages.append(AIMessage(content=clinician_response))

            self.updated_at = self._get_timestamp()
            if self._should_end_conversation(companion_response, clinician_response):
                langfuse_handler.flush()
                break

        langfuse_handler.flush()

    def _should_end_conversation(self, bot_msg: str, clinician_msg: str) -> bool:
        """Determines if the conversation should end based on the messages."""
        ending_phrases = ["goodbye", "bye", "see you", "take care"]
        return any(
            phrase in bot_msg.lower() or phrase in clinician_msg.lower()
            for phrase in ending_phrases
        )
