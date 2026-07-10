# Personal AI Assistant

A production-inspired, CLI-based AI assistant built with Python and the Groq API.
This is **Phase 1** of a larger roadmap that will eventually add RAG, memory,
tool calling, AI agents, and a web interface.

## Features (Phase 1)

- Terminal chat loop with a persistent system prompt
- Conversation history saved to disk as JSON
- Commands: `/new`, `/history`, `/load`, `/delete`, `/clear`, `/help`, `/exit`
- Centralized config and logging
- Clean separation of concerns (client / conversation / assistant / CLI)

## Project Structure

```
personal-ai-assistant/
├── app.py                 # CLI entry point
├── config.py               # Central configuration
├── chatbot/
│   ├── assistant.py         # Orchestrates client + conversation
│   ├── client.py            # Talks to the Groq API
│   ├── conversation.py      # Conversation state + persistence
│   ├── prompts.py           # System prompt
│   ├── stream.py            # (Phase 3) streaming responses
│   └── search.py            # (Phase 5) RAG / search
├── data/
│   ├── conversations/        # Saved chats (JSON)
│   └── settings.json
└── utils/
    ├── helpers.py            # IDs, timestamps, validation
    └── logger.py             # Logging setup
```

## Setup

```bash
git clone https://github.com/Shaila-Yasin/personal_assistant
cd personal-ai-assistant
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env       # then add your GROQ_API_KEY
python app.py
```

## Roadmap

- [x] Phase 1 — CLI chatbot
- [ ] Phase 2 — Conversation management (mostly done, search pending)
- [ ] Phase 3 — Streaming responses
- [ ] Phase 4 — Enhanced CLI
- [ ] Phase 5 — RAG (ChromaDB / FAISS)
- [ ] Phase 6 — Long-term memory
- [ ] Phase 7 — Tool calling
- [ ] Phase 8 — AI agents
- [ ] Phase 9 — Web interface

## Tech Stack

Python 3.12 · Groq API · python-dotenv · JSON

## Author 
*Shaila Yasin*

## GitHub
https://github.com/Shaila-Yasin
