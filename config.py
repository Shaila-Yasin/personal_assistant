"""
config.py

Central configuration for the whole application.

Every other module reads its settings from here instead of calling
os.getenv(...) directly. That way, if we ever change *how* config is
loaded (e.g. move to a YAML file, or add a settings UI), we only edit
this one file.
"""

import os
from dotenv import load_dotenv

# Load variables from a local .env file into the environment.
# This must run before we read any os.getenv() calls below.
load_dotenv()

# --- Groq / LLM settings -----------------------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# You can swap this for any model Groq currently serves
# (e.g. "llama-3.1-8b-instant" for a faster/cheaper option).
MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Controls randomness of the model's output. 0 = deterministic, 1+ = creative.
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))

# Maximum tokens the model is allowed to generate in a single reply.
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))

# --- Application settings -----------------------------------------------

APP_NAME = "Personal AI Assistant"

# Where conversation JSON files and settings.json live.
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CONVERSATIONS_DIR = os.path.join(DATA_DIR, "conversations")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

# Fail fast with a clear message instead of a confusing traceback later.
if not GROQ_API_KEY:
    raise EnvironmentError(
        "GROQ_API_KEY is missing. Create a .env file in the project root "
        "with a line like: GROQ_API_KEY=your_key_here"
    )
