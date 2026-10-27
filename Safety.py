"""safety.py - classifies what the visitor typed. NOTHING here ever runs a command."""
import re

# (pattern, why it is dangerous)
DANGEROUS = [
    (r"\brm\s+-[a-z]*r[a-z]*f|\brm\s+-[a-z]*f[a-z]*r", "Force-deletes files and folders recursively. Data can be lost forever."),
    (r"\bdel\s+/[sqf]", "Deletes files without asking. Data can be lost."),
    (r"\bformat\s+[a-z]:", "Wipes an entire drive."),
    (r"\bmkfs", "Creates a new filesystem and erases the old one."),
    (r"\bdd\s+if=", "Writes raw data to disks and can overwrite everything."),
    (r"\bshutdown\b", "Turns the computer off."),
    (r":\(\)\s*\{", "A 'fork bomb' that can freeze the computer."),
    (r"chmod\s+-r\s+777", "Makes everything open to everyone - a security risk."),
    (r"(curl|wget).*\|\s*(sh|bash)", "Downloads a script and runs it blindly."),
]

# Harmless commands the ghost can explain
KNOWN = {
    "ls": "Lists files in a folder.",
    "dir": "Lists files in a folder (Windows).",
    "cd": "Moves into another folder.",
    "pwd": "Shows the current folder.",
    "cat": "Prints what is inside a file.",
    "whoami": "Shows the current user.",
    "ping": "Tests whether another machine answers.",
    "help": "Asks the ghost for help.",
    "ps": "Lists running programs.",
    "top": "Shows what is using the computer's power.",
}


def classify(text: str) -> dict:
    """Return {'level': 'dangerous' | 'known' | 'chat', 'note': str}."""
    t = text.strip().lower()
    for pattern, why in DANGEROUS:
        if re.search(pattern, t):
            return {"level": "dangerous", "note": why}
    first = t.split()[0] if t.split() else ""
    if first in KNOWN:
        return {"level": "known", "note": KNOWN[first]}
    return {"level": "chat", "note": ""}