"""
chatbot/assistant.py

The "brain" of the application. Coordinates everything but doesn't do
any I/O itself (no print, no input()) — it just takes a prompt in and
hands a response back to app.py.

Flow for a single turn:

    user prompt -> Conversation (add message)
                -> GroqClient (get_response)
                -> Conversation (store reply)
                -> return reply to caller
"""

from chatbot.client import GroqClient
from chatbot.conversation import Conversation
from utils.logger import get_logger

logger = get_logger(__name__)


class Assistant:
    def __init__(self, conversation: Conversation | None = None):
        self.client = GroqClient()
        self.conversation = conversation or Conversation()

    def ask(self, user_input: str) -> str:
        """Send one user message through the full pipeline and return the reply."""
        self.conversation.add_user_message(user_input)

        reply = self.client.get_response(self.conversation.get_messages())

        self.conversation.add_assistant_message(reply)
        logger.info("Exchanged one message turn.")

        return reply

    def new_conversation(self) -> None:
        """Discard the current conversation and start a fresh one."""
        self.conversation = Conversation()

    def load_conversation(self, conversation_id: str) -> None:
        self.conversation = Conversation.load(conversation_id)

    def save_conversation(self) -> str:
        return self.conversation.save()
