# 👻 GhostShell AI

A haunted terminal where a ghost named Wisp answers you, powered by a **local open-weight model (Gemma 3 via Ollama)**.
Commands you type are **never executed** - they are only explained, and dangerous ones are flagged.

## Why open innovation?
- Runs locally: prompts stay on your laptop.
- Works offline after setup.
- Model is configurable (gemma3:1b, gemma3:4b, ...).

## Setup (Windows)
1. Install Ollama from https://ollama.com/download/windows
2. `ollama pull gemma3:1b`
3. In PowerShell:
   ```
   py -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   streamlit run app.py
   ```

## Tests
`python tests/test_safety.py`

## Measured latency (my laptop)
_Fill in your real numbers here._

## Model & license
Gemma 3 - see the Gemma terms of use. _Add the exact link._

## Safety design
`safety.py` only classifies text. No input is ever passed to a shell.