"""
chatbot/client.py

The ONLY file that talks to Groq's API.

Responsibilities:
- Open a connection to Groq.
- Send a list of conversation messages.
- Return the model's reply as plain text.

It deliberately knows nothing about the CLI, JSON files, or conversation
history management. That separation means we could later swap Groq for
OpenAI or a local model by rewriting just this file.
"""

from groq import Groq
from groq import GroqError

from config import GROQ_API_KEY, MODEL_NAME, TEMPERATURE, MAX_TOKENS
from utils.logger import get_logger

logger = get_logger(__name__)


class GroqClient:
    """Thin wrapper around the Groq SDK."""

    def __init__(self):
        self._client = Groq(api_key=GROQ_API_KEY)

    def get_response(self, messages: list[dict]) -> str:
        """
        Send the full message history to Groq and return the assistant's
        reply as a string.

        messages: a list of {"role": "system"|"user"|"assistant", "content": str}
                  following the standard chat-completions format.
        """
        try:
            completion = self._client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
            )
            return completion.choices[0].message.content

        except GroqError as e:
            # Log the real error for debugging, but keep the app alive
            # and hand the caller a friendly message instead of crashing.
            logger.error(f"Groq API error: {e}")
            return "Sorry, I ran into an error talking to the AI service. Please try again."

        except Exception as e:
            logger.error(f"Unexpected error in GroqClient: {e}")
            return "Something went wrong while generating a response."
