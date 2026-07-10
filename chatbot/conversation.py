"""
chatbot/conversation.py

Manages a single conversation's state and its persistence to disk.

Responsibilities:
- Hold the running list of messages for the current chat.
- Add user / assistant messages.
- Save the conversation to data/conversations/<id>.json
- Load a saved conversation back into memory.
- List and delete saved conversations.

This file does NOT talk to the LLM and does NOT print anything to the
screen — it only manages state. app.py decides what to display.
"""

import json
import os

from chatbot.prompts import SYSTEM_PROMPT
from config import CONVERSATIONS_DIR
from utils.helpers import generate_id, now_timestamp
from utils.logger import get_logger

logger = get_logger(__name__)


class Conversation:
    def __init__(self, conversation_id: str | None = None):
        self.id = conversation_id or generate_id()
        self.created_at = now_timestamp()
        self.messages: list[dict] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    # --- message handling -------------------------------------------------

    def add_user_message(self, content: str) -> None:
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str) -> None:
        self.messages.append({"role": "assistant", "content": content})

    def get_messages(self) -> list[dict]:
        """Return the full message list, ready to send to the LLM."""
        return self.messages

    # --- persistence --------------------------------------------------

    def save(self) -> str:
        """Write this conversation to disk as JSON. Returns the file path."""
        os.makedirs(CONVERSATIONS_DIR, exist_ok=True)
        path = os.path.join(CONVERSATIONS_DIR, f"{self.id}.json")

        data = {
            "id": self.id,
            "created_at": self.created_at,
            "messages": self.messages,
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved conversation {self.id}")
        return path

    @classmethod
    def load(cls, conversation_id: str) -> "Conversation":
        """Load a conversation from disk by its id."""
        path = os.path.join(CONVERSATIONS_DIR, f"{conversation_id}.json")

        if not os.path.exists(path):
            raise FileNotFoundError(f"No conversation found with id '{conversation_id}'")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        convo = cls(conversation_id=data["id"])
        convo.created_at = data["created_at"]
        convo.messages = data["messages"]
        return convo

    @staticmethod
    def list_all() -> list[str]:
        """Return the ids of every saved conversation, newest first."""
        if not os.path.exists(CONVERSATIONS_DIR):
            return []

        files = [f for f in os.listdir(CONVERSATIONS_DIR) if f.endswith(".json")]
        files.sort(key=lambda f: os.path.getmtime(os.path.join(CONVERSATIONS_DIR, f)), reverse=True)
        return [f.removesuffix(".json") for f in files]

    @staticmethod
    def delete(conversation_id: str) -> bool:
        """Delete a saved conversation. Returns True if it existed."""
        path = os.path.join(CONVERSATIONS_DIR, f"{conversation_id}.json")
        if os.path.exists(path):
            os.remove(path)
            logger.info(f"Deleted conversation {conversation_id}")
            return True
        return False
