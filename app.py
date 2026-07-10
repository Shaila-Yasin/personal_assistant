"""
app.py

Entry point of the application.

Responsibilities:
- Start the app and print the banner.
- Read user input in a loop.
- Handle CLI commands (/help, /new, /history, /load, /delete, /clear, /exit).
- Display AI responses.

This file intentionally contains very little logic. All the real work
(talking to the LLM, managing conversation state) happens in the
`chatbot` package. app.py is just the terminal "view".
"""

from chatbot.assistant import Assistant
from chatbot.conversation import Conversation
from utils.helpers import is_valid_input, format_timestamp
from config import APP_NAME

BANNER = f"""
======================================================
🤖 {APP_NAME}
Type /help for available commands.
======================================================
"""

HELP_TEXT = """
Available commands:
  /new       Start a new conversation (unsaved changes are lost)
  /history   List all saved conversations
  /load <id> Load a saved conversation by its id
  /delete <id>  Delete a saved conversation by its id
  /clear     Clear the terminal screen
  /help      Show this help message
  /exit      Save the current conversation and quit
"""


def print_history() -> None:
    ids = Conversation.list_all()
    if not ids:
        print("No saved conversations yet.")
        return
    print("Saved conversations:")
    for cid in ids:
        print(f"  - {cid}")


def handle_command(command: str, assistant: Assistant) -> bool:
    """
    Handle a slash command. Returns False if the app should exit,
    True otherwise.
    """
    parts = command.strip().split(maxsplit=1)
    cmd = parts[0].lower()
    arg = parts[1].strip() if len(parts) > 1 else None

    if cmd == "/help":
        print(HELP_TEXT)

    elif cmd == "/new":
        assistant.new_conversation()
        print("Started a new conversation.\n")

    elif cmd == "/history":
        print_history()

    elif cmd == "/load":
        if not arg:
            print("Usage: /load <conversation_id>")
        else:
            try:
                assistant.load_conversation(arg)
                print(f"Loaded conversation '{arg}'.\n")
            except FileNotFoundError as e:
                print(str(e))

    elif cmd == "/delete":
        if not arg:
            print("Usage: /delete <conversation_id>")
        else:
            deleted = Conversation.delete(arg)
            print("Deleted." if deleted else f"No conversation found with id '{arg}'.")

    elif cmd == "/clear":
        print("\n" * 100)

    elif cmd == "/exit":
        path = assistant.save_conversation()
        print(f"Conversation saved to {path}. Goodbye!")
        return False

    else:
        print(f"Unknown command: {cmd}. Type /help to see available commands.")

    return True


def main() -> None:
    print(BANNER)
    assistant = Assistant()

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            assistant.save_conversation()
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            should_continue = handle_command(user_input, assistant)
            if not should_continue:
                break
            continue

        if not is_valid_input(user_input):
            print("Please enter a valid message.")
            continue

        reply = assistant.ask(user_input)
        print(f"\nA:\n{reply}\n")


if __name__ == "__main__":
    main()
