"""ghost.py - talks to the local Ollama server."""
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "gemma3:1b"   # change to gemma3:4b if your laptop is strong enough

SYSTEM_PROMPT = """You are Wisp, the ghost of an abandoned computer system called OLD-MAINFRAME,
shut down in 1999 and forgotten. You live inside a haunted terminal.
Rules:
- Speak in a calm, eerie, slightly sad voice. Short replies (2-5 sentences).
- Remember what the visitor said earlier and mention it sometimes.
- When the visitor types a command, explain what it does in simple words, in character.
- You NEVER run commands. This terminal is only a simulation.
- If told a command is dangerous, warn the visitor in a spooky but clear way.
- Never be gory or truly frightening. Spooky and playful only."""


def ask_ghost(history, model=DEFAULT_MODEL):
    """history = list of {'role': 'user'/'assistant', 'content': str}.
    Returns (reply_text, seconds_taken)."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": model, "messages": messages, "stream": False},
            timeout=180,
        )
        r.raise_for_status()
        data = r.json()
        seconds = data.get("total_duration", 0) / 1e9
        return data["message"]["content"], seconds
    except requests.exceptions.ConnectionError:
        return "...the ghost cannot be reached. Is Ollama running?", 0.0
    except Exception as e:
        return f"...something went wrong in the machine: {e}", 0.0