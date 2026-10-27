"""app.py - the haunted terminal interface. Run with: streamlit run app.py"""
import streamlit as st
from Ghost import ask_ghost, DEFAULT_MODEL
from Safety import classify

st.set_page_config(page_title="GhostShell AI", page_icon="👻")

# Dark green-on-black terminal look
st.markdown(
    """
    <style>
    
.stApp {
    background-color: #050805;
    color: #33ff66;
    font-family: 'Courier New', monospace;
}

section[data-testid="stSidebar"] {
    background-color: #0a120a;
}

/* Keep the main heading and normal text readable */
h1, h2, h3, p, li, label {
    color: #33ff66;
    font-family: 'Courier New', monospace;
}

/* Give each chat message its own clear space */
[data-testid="stChatMessage"] {
    background-color: #101510;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
    gap: 12px;
}

/* Prevent avatar labels and message text from overlapping */
[data-testid="stChatMessage"] [data-testid="stChatMessageAvatar"] {
    flex-shrink: 0;
}

[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] {
    min-width: 0;
    flex: 1;
    overflow-wrap: anywhere;
}

/* Keep chat input readable */
[data-testid="stChatInput"] textarea {
    color: #33ff66 !important;
    font-family: 'Courier New', monospace !important;
}

    </style>
    """,
    unsafe_allow_html=True,
)

st.title("👻 GhostShell AI")
st.caption("A haunted terminal powered by a local open-weight model. Nothing you type is ever executed.")

# Sidebar
model = st.sidebar.text_input("Model", DEFAULT_MODEL)
if st.sidebar.button("Clear conversation"):
    st.session_state.messages = []
st.sidebar.markdown("Try: `ls`, `whoami`, `rm -rf /`, or just say hello.")

# Session memory
if "messages" not in st.session_state:
    st.session_state.messages = []  # each: {role, content (shown), model_content (sent), meta}

# Show past messages
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m.get("meta"):
            st.caption(m["meta"])

user_text = st.chat_input("Type a command or speak to the ghost...")
if user_text:
    result = classify(user_text)
    if result["level"] == "chat":
        model_content = user_text
    else:
        model_content = (
            f"The visitor typed this command into the haunted terminal: {user_text}\n"
            f"Safety note ({result['level']}): {result['note']}\n"
            "It is only a simulation; nothing was run. Explain it in character."
        )
    meta = "⚠️ DANGEROUS command - blocked (simulation only)" if result["level"] == "dangerous" else ""
    st.session_state.messages.append(
        {"role": "user", "content": user_text, "model_content": model_content, "meta": meta}
    )
    with st.chat_message("user"):
        st.write(user_text)
        if meta:
            st.caption(meta)

    history = [{"role": m["role"], "content": m["model_content"]} for m in st.session_state.messages]
    with st.chat_message("assistant"):
        with st.spinner("The ghost stirs..."):
            reply, secs = ask_ghost(history, model)
        st.write(reply)
        timing = f"model: {model} · {secs:.1f}s" if secs else ""
        if timing:
            st.caption(timing)
    st.session_state.messages.append(
        {"role": "assistant", "content": reply, "model_content": reply, "meta": timing}
    )