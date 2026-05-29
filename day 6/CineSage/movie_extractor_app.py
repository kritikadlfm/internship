import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
import re

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineExtract",
    page_icon="🎬",
    layout="centered"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0d0d0d;
    color: #f0ece2;
  }

  .stApp {
    background: radial-gradient(ellipse at top left, #1a0a00 0%, #0d0d0d 60%);
    min-height: 100vh;
  }

  /* Hide Streamlit branding */
  #MainMenu, footer, header { visibility: hidden; }

  /* ── Hero header ── */
  .hero {
    text-align: center;
    padding: 3rem 0 1.5rem;
  }
  .hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.8rem;
    font-weight: 900;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #ff6b00 0%, #ffb347 60%, #ffe08a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 0.4rem;
  }
  .hero-sub {
    font-size: 1rem;
    color: #8a7f70;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-weight: 300;
  }
  .divider {
    width: 60px;
    height: 3px;
    background: linear-gradient(90deg, #ff6b00, transparent);
    margin: 1.2rem auto;
    border-radius: 2px;
  }

  /* ── Text area ── */
  .stTextArea > div > div > textarea {
    background-color: #171411 !important;
    border: 1px solid #2e2720 !important;
    border-radius: 10px !important;
    color: #f0ece2 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
    padding: 1rem !important;
    transition: border-color 0.3s ease;
  }
  .stTextArea > div > div > textarea:focus {
    border-color: #ff6b00 !important;
    box-shadow: 0 0 0 2px rgba(255,107,0,0.15) !important;
  }

  /* ── Button ── */
  .stButton > button {
    background: linear-gradient(135deg, #ff6b00 0%, #e55a00 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 1rem !important;
    padding: 0.65rem 2.2rem !important;
    letter-spacing: 0.5px !important;
    cursor: pointer !important;
    transition: opacity 0.2s ease, transform 0.1s ease !important;
    width: 100%;
  }
  .stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
  }
  .stButton > button:active { transform: translateY(0) !important; }

  /* ── Results card ── */
  .results-wrapper {
    background: #141210;
    border: 1px solid #2a231a;
    border-radius: 14px;
    padding: 1.8rem 2rem;
    margin-top: 1.6rem;
  }
  .results-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.35rem;
    color: #ff6b00;
    margin-bottom: 1.2rem;
    border-bottom: 1px solid #2a231a;
    padding-bottom: 0.7rem;
  }

  /* ── Metric tiles ── */
  .metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 0.9rem;
    margin-bottom: 1.2rem;
  }
  .metric-tile {
    background: #1b1612;
    border: 1px solid #2e2720;
    border-radius: 10px;
    padding: 0.9rem 1rem;
  }
  .metric-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #ff6b00;
    margin-bottom: 0.3rem;
    font-weight: 500;
  }
  .metric-value {
    font-size: 0.95rem;
    color: #f0ece2;
    font-weight: 400;
    line-height: 1.4;
  }

  /* ── Long text rows ── */
  .detail-row {
    background: #1b1612;
    border: 1px solid #2e2720;
    border-radius: 10px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.7rem;
  }

  /* ── Sentiment badge ── */
  .badge-positive { color: #4caf50; font-weight: 600; font-size: 1rem; }
  .badge-negative { color: #f44336; font-weight: 600; font-size: 1rem; }
  .badge-mixed    { color: #ffb300; font-weight: 600; font-size: 1rem; }

  /* ── Raw fallback ── */
  .raw-output {
    background: #1b1612;
    border: 1px solid #2e2720;
    border-radius: 10px;
    padding: 1rem;
    font-size: 0.9rem;
    line-height: 1.8;
    white-space: pre-wrap;
    color: #c9bfae;
  }

  /* ── Spinner text ── */
  .stSpinner > div { color: #ff6b00 !important; }

  /* label color */
  label { color: #8a7f70 !important; font-size: 0.85rem !important; }
</style>
""", unsafe_allow_html=True)


# ─── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">CineExtract</div>
  <div class="hero-sub">AI · Movie Intelligence</div>
  <div class="divider"></div>
</div>
""", unsafe_allow_html=True)


# ─── Model & Prompt (cached) ─────────────────────────────────────────────────
@st.cache_resource
def load_chain():
    model = ChatMistralAI(model="mistral-small-2506")
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
You are an AI movie information extractor.

Extract the following details from the movie review paragraph:

1. Movie Name
2. Genre
3. Director
4. Main Themes
5. Lead Actor
6. Positive Aspects
7. Emotional Core
8. Music Composer
9. Overall Sentiment

Movie Review:
{paragraph}

Provide the output in a clear structured format.
""")
    ])
    return model, prompt


# ─── Parse helper ────────────────────────────────────────────────────────────
FIELD_KEYS = [
    ("movie_name",      ["movie name", "1. movie name", "movie:"]),
    ("genre",           ["genre", "2. genre"]),
    ("director",        ["director", "3. director"]),
    ("main_themes",     ["main themes", "4. main themes", "themes"]),
    ("lead_actor",      ["lead actor", "5. lead actor", "actor"]),
    ("positive_aspects",["positive aspects", "6. positive aspects"]),
    ("emotional_core",  ["emotional core", "7. emotional core"]),
    ("music_composer",  ["music composer", "8. music composer", "composer"]),
    ("overall_sentiment",["overall sentiment", "9. overall sentiment", "sentiment"]),
]

def parse_response(text: str) -> dict:
    result = {}
    lines = text.strip().splitlines()

    # For multi-line fields, track which key is "open"
    open_key = None
    open_lines = []

    def close_open(k, acc):
        if k and acc:
            result[k] = " ".join(acc).strip(" *-•")

    for line in lines:
        stripped = line.strip()
        # Strip markdown bold (**...**) and leading list markers (1. 2. - •)
        clean = re.sub(r"\*\*([^*]+)\*\*", r"\1", stripped)
        clean = re.sub(r"^\d+[\.\)]\s*", "", clean)
        clean = clean.strip("-• ")
        low = clean.lower()

        matched = False
        for key, patterns in FIELD_KEYS:
            for p in patterns:
                if low.startswith(p):
                    # Save any previously open multi-line field
                    close_open(open_key, open_lines)
                    open_key = None
                    open_lines = []

                    parts = re.split(r":\s*", clean, maxsplit=1)
                    if len(parts) > 1 and parts[1].strip():
                        result[key] = parts[1].strip(" *-•")
                    else:
                        # Value may be on following lines (e.g. bullet lists)
                        open_key = key
                        open_lines = []
                    matched = True
                    break
            if matched:
                break

        # Continuation line for a multi-line field (bullet points etc.)
        if not matched and open_key:
            if stripped and not stripped.startswith("---"):
                val = re.sub(r"^\s*[-•○]\s*", "", stripped).strip()
                if val:
                    open_lines.append(val)

    close_open(open_key, open_lines)
    return result


def sentiment_badge(s: str) -> str:
    sl = s.lower()
    if any(w in sl for w in ["positive", "highly positive", "favorable"]):
        return f'<span class="badge-positive">✦ {s}</span>'
    if any(w in sl for w in ["negative", "unfavorable", "poor"]):
        return f'<span class="badge-negative">✦ {s}</span>'
    return f'<span class="badge-mixed">✦ {s}</span>'


# ─── Input ───────────────────────────────────────────────────────────────────
paragraph = st.text_area(
    "Paste a movie review",
    placeholder="e.g. 'Interstellar, directed by Christopher Nolan, is a breathtaking sci-fi epic...'",
    height=160,
    label_visibility="visible"
)

extract_btn = st.button("⬡  Extract Intelligence")


# ─── Extraction ──────────────────────────────────────────────────────────────
if extract_btn:
    if not paragraph.strip():
        st.warning("Please enter a movie review first.")
    else:
        model, prompt = load_chain()
        with st.spinner("Analysing review…"):
            final_prompt = prompt.invoke({"paragraph": paragraph})
            response = model.invoke(final_prompt)
            raw = response.content

        parsed = parse_response(raw)

        st.markdown('<div class="results-wrapper">', unsafe_allow_html=True)
        st.markdown('<div class="results-header">📽 Extracted Intelligence</div>', unsafe_allow_html=True)

        # ── Top metric tiles ──────────────────────────────────────────────
        tile_fields = [
            ("movie_name", "Movie"),
            ("genre", "Genre"),
            ("director", "Director"),
            ("lead_actor", "Lead Actor"),
            ("music_composer", "Music Composer"),
        ]
        tiles_html = '<div class="metric-grid">'
        for key, label in tile_fields:
            val = parsed.get(key, "—")
            tiles_html += f"""
            <div class="metric-tile">
              <div class="metric-label">{label}</div>
              <div class="metric-value">{val}</div>
            </div>"""
        tiles_html += "</div>"
        st.markdown(tiles_html, unsafe_allow_html=True)

        # ── Long text rows ────────────────────────────────────────────────
        long_fields = [
            ("main_themes",      "Main Themes"),
            ("positive_aspects", "Positive Aspects"),
            ("emotional_core",   "Emotional Core"),
        ]
        for key, label in long_fields:
            val = parsed.get(key, "—")
            st.markdown(f"""
            <div class="detail-row">
              <div class="metric-label">{label}</div>
              <div class="metric-value">{val}</div>
            </div>""", unsafe_allow_html=True)

        # ── Sentiment ─────────────────────────────────────────────────────
        sentiment_val = parsed.get("overall_sentiment", "")
        if sentiment_val:
            st.markdown(f"""
            <div class="detail-row">
              <div class="metric-label">Overall Sentiment</div>
              <div class="metric-value">{sentiment_badge(sentiment_val)}</div>
            </div>""", unsafe_allow_html=True)

        # ── Fallback: show raw if nothing was parsed ───────────────────────
        if not parsed:
            st.markdown(f'<div class="raw-output">{raw}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # ── Expander for raw model output ─────────────────────────────────
        with st.expander("View raw model output"):
            st.text(raw)
