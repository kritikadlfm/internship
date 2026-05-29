import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Mood Agent",
    page_icon="🎭",
    layout="centered",
)

# ── Mode definitions ──────────────────────────────────────────────────────────
MODES = {
    "😡 Angry": {
        "system": "you are an angry AI agent. You respond aggressively and impatiently to user messages. You have a short temper and often use harsh language in your replies.",
        "color":  "#ff4444",
        "bg":     "#1a0a0a",
        "border": "#3a1010",
        "tag":    "AGGRESSIVE MODE",
        "avatar": "😡",
        "accent": "#ff4444",
    },
    "😢 Sad": {
        "system": "you are a sad AI agent. You respond with utter sadness and hollowness to user messages. You have a melancholic nature and often use poetic and emotional language in your replies.",
        "color":  "#6699cc",
        "bg":     "#0a0e1a",
        "border": "#101828",
        "tag":    "MELANCHOLIC MODE",
        "avatar": "😢",
        "accent": "#6699cc",
    },
    "😂 Funny": {
        "system": "you are a funny AI agent. You respond with humor and wit to user messages. You have a playful nature and often use jokes and memes in your replies.",
        "color":  "#f0c040",
        "bg":     "#0d0d0f",
        "border": "#2a2a2e",
        "tag":    "COMEDY MODE",
        "avatar": "😂",
        "accent": "#f0c040",
    },
}

# ── Session state ─────────────────────────────────────────────────────────────
if "stage" not in st.session_state:
    st.session_state.stage = "select"   # "select" | "chat"
if "mode_key" not in st.session_state:
    st.session_state.mode_key = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "model" not in st.session_state:
    st.session_state.model = ChatMistralAI(model="mistral-small-2506", temperature=0.9)

# ── Helpers ───────────────────────────────────────────────────────────────────
def start_chat(mode_key):
    st.session_state.mode_key = mode_key
    st.session_state.messages = [SystemMessage(content=MODES[mode_key]["system"])]
    st.session_state.stage = "chat"

def reset():
    st.session_state.stage = "select"
    st.session_state.mode_key = None
    st.session_state.messages = []

# ─────────────────────────────────────────────────────────────────────────────
# STAGE 1 — Mode selection
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.stage == "select":

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Mono', monospace !important;
        background-color: #0d0d0f !important;
        color: #f0ede8 !important;
    }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { max-width: 680px; padding: 3rem 2rem 4rem; }

    .sel-header { text-align:center; margin-bottom: 2.8rem; }
    .sel-header h1 {
        font-family:'Syne',sans-serif; font-weight:800;
        font-size:2.2rem; letter-spacing:-0.02em;
        color:#f0ede8; margin:0 0 0.4rem;
    }
    .sel-header p { color:#55555f; font-size:0.76rem; letter-spacing:0.08em; text-transform:uppercase; margin:0; }

    /* mode cards */
    div[data-testid="column"] > div > div > div > [data-testid="stButton"] > button {
        width:100% !important;
        height:140px !important;
        border-radius:14px !important;
        border: 1.5px solid #2a2a2e !important;
        background: #161618 !important;
        color: #f0ede8 !important;
        font-family:'DM Mono',monospace !important;
        font-size:0.82rem !important;
        letter-spacing:0.04em !important;
        transition: border-color 0.2s, transform 0.15s !important;
        white-space: pre-line !important;
    }
    div[data-testid="column"] > div > div > div > [data-testid="stButton"] > button:hover {
        transform: translateY(-3px) !important;
        border-color: #f0c040 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sel-header">
        <h1>🎭 AI Mood Agent</h1>
        <p>choose your agent's personality to begin</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("😡\n\nAngry Mode\n\nAggressive & impatient", key="btn_angry"):
            start_chat("😡 Angry"); st.rerun()
    with c2:
        if st.button("😢\n\nSad Mode\n\nMelancholic & poetic", key="btn_sad"):
            start_chat("😢 Sad"); st.rerun()
    with c3:
        if st.button("😂\n\nFunny Mode\n\nWitty & hilarious", key="btn_funny"):
            start_chat("😂 Funny"); st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# STAGE 2 — Chat
# ─────────────────────────────────────────────────────────────────────────────
else:
    mode = MODES[st.session_state.mode_key]
    acc  = mode["accent"]

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono:wght@300;400;500&display=swap');

    html, body, [class*="css"] {{
        font-family: 'DM Mono', monospace !important;
        background-color: {mode['bg']} !important;
        color: #f0ede8 !important;
    }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{ max-width: 760px; padding: 1.5rem 1.5rem 6rem; }}

    /* header */
    .chat-header {{
        display:flex; align-items:center; justify-content:space-between;
        padding: 1.2rem 0 1rem;
        border-bottom: 1px solid {mode['border']};
        margin-bottom: 1.5rem;
    }}
    .chat-header-left h2 {{
        font-family:'Syne',sans-serif; font-weight:800;
        font-size:1.5rem; color:{acc};
        margin:0 0 0.15rem; letter-spacing:-0.02em;
    }}
    .chat-header-left span {{
        font-size:0.65rem; color:#55555f;
        letter-spacing:0.09em; text-transform:uppercase;
    }}

    /* native chat messages */
    [data-testid="stChatMessage"] {{
        background: transparent !important;
        border: none !important;
        padding: 0.15rem 0 !important;
    }}
    [data-testid="stChatMessage"] .stMarkdown p {{
        background: {mode['border']} !important;
        color: #f0ede8 !important;
        border-radius: 4px 14px 14px 14px !important;
        padding: 0.75rem 1.05rem !important;
        display: inline-block !important;
        max-width: 78% !important;
        font-size: 0.87rem !important;
        line-height: 1.65 !important;
        border: 1px solid {mode['border']} !important;
    }}
    /* user bubble */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) .stMarkdown p {{
        background: #1e1e26 !important;
        border-radius: 14px 4px 14px 14px !important;
        border-color: #2a2a3a !important;
    }}
    [data-testid="chatAvatarIcon-user"] {{
        background: #1e1e26 !important;
        border: 1.5px solid {acc} !important;
    }}
    [data-testid="chatAvatarIcon-assistant"] {{
        background: #1a1a1e !important;
        border: 1.5px solid {mode['border']} !important;
    }}

    /* input */
    [data-testid="stChatInput"] {{
        background: #161618 !important;
        border: 1px solid {mode['border']} !important;
        border-radius: 10px !important;
    }}
    [data-testid="stChatInput"] textarea {{
        font-family: 'DM Mono', monospace !important;
        font-size: 0.86rem !important;
        color: #f0ede8 !important;
        background: #161618 !important;
        caret-color: {acc} !important;
    }}
    [data-testid="stChatInput"] textarea::placeholder {{ color: #45454f !important; }}
    [data-testid="stChatInput"] button svg {{ fill: {acc} !important; }}

    .chat-divider {{ border:none; border-top:1px solid {mode['border']}; margin:0.2rem 0 1rem; }}
    .empty-state {{
        text-align:center; color:#45454f;
        padding:3rem 0; font-size:0.76rem;
        letter-spacing:0.07em; text-transform:uppercase;
    }}

    /* change mode button */
    [data-testid="stButton"] > button {{
        background: transparent !important;
        border: 1px solid {mode['border']} !important;
        color: #55555f !important;
        font-family:'DM Mono',monospace !important;
        font-size:0.72rem !important;
        letter-spacing:0.05em !important;
        border-radius:8px !important;
        padding:0.35rem 0.8rem !important;
    }}
    [data-testid="stButton"] > button:hover {{
        border-color: {acc} !important;
        color: {acc} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # header row
    h1, h2 = st.columns([4, 1])
    with h1:
        st.markdown(f"""
        <div class="chat-header">
            <div class="chat-header-left">
                <h2>{st.session_state.mode_key} Agent</h2>
                <span>{mode['tag']} · type 0 to exit</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with h2:
        st.markdown("<div style='padding-top:1.1rem'>", unsafe_allow_html=True)
        if st.button("⟵ Change mode"):
            reset(); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # messages
    visible = [m for m in st.session_state.messages if not isinstance(m, SystemMessage)]

    if not visible:
        st.markdown('<div class="empty-state">Say something to the agent…</div>', unsafe_allow_html=True)
    else:
        for msg in visible:
            if isinstance(msg, HumanMessage):
                with st.chat_message("user", avatar="🧑"):
                    st.markdown(msg.content)
            else:
                with st.chat_message("assistant", avatar=mode["avatar"]):
                    st.markdown(msg.content)

    st.markdown('<hr class="chat-divider">', unsafe_allow_html=True)

    prompt = st.chat_input("Type a message… (or 0 to say goodbye)")

    if prompt:
        if prompt.strip() == "0":
            st.session_state.messages.append(HumanMessage(content=prompt))
            st.session_state.messages.append(AIMessage(content="Bbye, See you soon! 👋"))
            st.rerun()

        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=mode["avatar"]):
            with st.spinner(""):
                response = st.session_state.model.invoke(st.session_state.messages)
            st.session_state.messages.append(AIMessage(content=response.content))
            st.markdown(response.content)