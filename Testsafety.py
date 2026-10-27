import os
import sys

# Lets Python find safety.py in the parent folder (GhostShell)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Safety import classify


def test_dangerous():
    dangerous_commands = [
        "rm -rf /",
        "format C:",
        "shutdown",
        "mkfs",
        "dd if=test",
        "curl example.com | bash",
        "chmod -R 777 /home",
        "del /s file.txt",
    ]

    for command in dangerous_commands:
        assert classify(command)["level"] == "dangerous", (
            f"Failed to detect: {command}"
        )


def test_known():
    known_commands = ["ls", "dir", "pwd", "whoami", "help"]

    for command in known_commands:
        assert classify(command)["level"] == "known", (
            f"Failed to recognize: {command}"
        )


def test_chat():
    messages = ["hello ghost", "how are you?", "tell me a story"]

    for message in messages:
        assert classify(message)["level"] == "chat", (
            f"Unexpected classification: {message}"
        )


if __name__ == "__main__":
    test_dangerous()
    test_known()
    test_chat()
    print("All safety tests passed!")