import streamlit as st
from dotenv import load_dotenv
load_dotenv()

import json
from pydantic import BaseModel
from typing import List, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import PydanticOutputParser

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ReelParse",
    page_icon="🎞",
    layout="centered"
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600&display=swap');

  html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    background-color: #08080f;
    color: #e8e4f0;
  }

  .stApp {
    background: #08080f;
    background-image:
      radial-gradient(ellipse 80% 40% at 50% -10%, rgba(99,20,220,0.18) 0%, transparent 70%),
      radial-gradient(ellipse 40% 30% at 90% 80%, rgba(220,20,99,0.1) 0%, transparent 60%);
    min-height: 100vh;
  }

  #MainMenu, footer, header { visibility: hidden; }

  /* ── Hero ── */
  .hero {
    text-align: center;
    padding: 2.8rem 0 1.2rem;
    position: relative;
  }
  .hero-eyebrow {
    font-size: 0.72rem;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: #8b5cf6;
    margin-bottom: 0.5rem;
    font-weight: 500;
  }
  .hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5.5rem;
    line-height: 0.92;
    letter-spacing: 4px;
    color: #f0ebff;
    text-shadow: 0 0 60px rgba(139,92,246,0.35);
    margin-bottom: 0.6rem;
  }
  .hero-title span {
    color: #c026d3;
  }
  .hero-desc {
    font-size: 0.9rem;
    color: #6b6080;
    font-weight: 300;
    max-width: 400px;
    margin: 0 auto;
    line-height: 1.6;
  }
  .strip {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, #3b1f6e, #c026d3, #3b1f6e, transparent);
    margin: 1.6rem 0;
    opacity: 0.6;
  }

  /* ── Input area ── */
  .stTextArea > div > div > textarea {
    background-color: #100f1a !important;
    border: 1px solid #2a1f4e !important;
    border-radius: 10px !important;
    color: #ddd8f0 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.93rem !important;
    line-height: 1.75 !important;
    padding: 1rem 1.1rem !important;
    caret-color: #8b5cf6 !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
  }
  .stTextArea > div > div > textarea:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.12) !important;
  }
  .stTextArea > div > div > textarea::placeholder { color: #3d3560 !important; }

  /* ── Button ── */
  .stButton > button {
    background: linear-gradient(135deg, #7c3aed 0%, #c026d3 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    padding: 0.7rem 2rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 4px 24px rgba(139,92,246,0.25) !important;
  }
  .stButton > button:hover { opacity: 0.85 !important; transform: translateY(-2px) !important; }
  .stButton > button:active { transform: translateY(0) !important; }

  /* ── Movie card shell ── */
  .movie-card {
    background: linear-gradient(145deg, #110e1e, #0d0b17);
    border: 1px solid #2a1f4e;
    border-radius: 16px;
    padding: 2rem 2.2rem;
    margin-top: 1.8rem;
    position: relative;
    overflow: hidden;
  }
  .movie-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #7c3aed, #c026d3, #7c3aed);
  }

  /* ── Movie title block ── */
  .movie-title-block {
    margin-bottom: 1.5rem;
  }
  .movie-main-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    letter-spacing: 2px;
    color: #f0ebff;
    line-height: 1;
    margin-bottom: 0.3rem;
  }
  .movie-year-badge {
    display: inline-block;
    background: rgba(139,92,246,0.18);
    border: 1px solid rgba(139,92,246,0.4);
    color: #a78bfa;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 2px;
    padding: 0.18rem 0.7rem;
    border-radius: 20px;
    text-transform: uppercase;
  }

  /* ── Info row ── */
  .info-row {
    display: flex;
    gap: 0.8rem;
    flex-wrap: wrap;
    margin-bottom: 1.4rem;
    align-items: center;
  }
  .info-chip {
    background: #1a1528;
    border: 1px solid #2e2250;
    border-radius: 6px;
    padding: 0.3rem 0.75rem;
    font-size: 0.82rem;
    color: #c4b8e8;
    font-weight: 400;
  }
  .info-chip.genre { border-color: rgba(192,38,211,0.4); color: #e879f9; background: rgba(192,38,211,0.08); }
  .info-chip.director { border-color: rgba(139,92,246,0.4); color: #a78bfa; background: rgba(139,92,246,0.08); }

  /* ── Rating ── */
  .rating-block {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1.4rem;
  }
  .rating-stars {
    font-size: 1.1rem;
    letter-spacing: 2px;
  }
  .rating-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: #fbbf24;
    letter-spacing: 1px;
  }
  .rating-outof {
    font-size: 0.8rem;
    color: #5a5070;
    font-weight: 300;
  }

  /* ── Section labels ── */
  .section-label {
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: #7c3aed;
    font-weight: 600;
    margin-bottom: 0.5rem;
  }

  /* ── Cast list ── */
  .cast-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1.4rem;
  }
  .cast-pill {
    background: #1a1528;
    border: 1px solid #2e2250;
    border-radius: 30px;
    padding: 0.28rem 0.85rem;
    font-size: 0.83rem;
    color: #c4b8e8;
  }

  /* ── Summary ── */
  .summary-box {
    background: #0f0d1a;
    border-left: 3px solid #7c3aed;
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.1rem;
    font-size: 0.9rem;
    line-height: 1.75;
    color: #b0a8cc;
    font-style: italic;
  }

  /* ── Divider ── */
  .inner-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, #2a1f4e, transparent);
    margin: 1.2rem 0;
  }

  /* ── Error / warning ── */
  .err-box {
    background: rgba(220,38,38,0.08);
    border: 1px solid rgba(220,38,38,0.3);
    border-radius: 8px;
    padding: 0.8rem 1rem;
    color: #fca5a5;
    font-size: 0.88rem;
  }

  label { color: #4e4470 !important; font-size: 0.84rem !important; }
</style>
""", unsafe_allow_html=True)


# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">Structured · AI · Extraction</div>
  <div class="hero-title">REEL<span>PARSE</span></div>
  <div class="hero-desc">Drop any movie paragraph and get clean, structured intelligence instantly.</div>
</div>
<div class="strip"></div>
""", unsafe_allow_html=True)


# ─── Schema & Chain (cached) ──────────────────────────────────────────────────
class Movie(BaseModel):
    title: str
    release_year: Optional[int] = None
    genre: List[str] = []
    director: Optional[str] = None
    cast: List[str] = []
    rating: Optional[float] = None
    summary: str

@st.cache_resource
def load_chain():
    model = ChatMistralAI(model="mistral-small-2506")
    parser = PydanticOutputParser(pydantic_object=Movie)
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
Extract movie information from the paragraph.
{format_instructions}
"""),
        ("human", "{paragraph}")
    ])
    return model, parser, prompt


# ─── Render Movie Card ────────────────────────────────────────────────────────
def render_stars(rating: float) -> str:
    full = int(rating // 2)
    half = 1 if (rating % 2) >= 1 else 0
    empty = 5 - full - half
    return "★" * full + ("½" if half else "") + "☆" * empty

def render_movie_card(movie: Movie):
    year_html = f'<span class="movie-year-badge">{movie.release_year}</span>' if movie.release_year else ""
    director_chip = f'<span class="info-chip director">🎬 {movie.director}</span>' if movie.director else ""

    genres_html = "".join(f'<span class="info-chip genre">{g}</span>' for g in movie.genre) if movie.genre else ""
    cast_html = "".join(f'<span class="cast-pill">{c}</span>' for c in movie.cast) if movie.cast else '<span style="color:#3d3560;font-size:0.85rem">Not specified</span>'

    rating_html = ""
    if movie.rating is not None:
        stars = render_stars(movie.rating)
        rating_html = f"""
        <div class="rating-block">
          <span class="rating-stars" style="color:#fbbf24">{stars}</span>
          <span class="rating-num">{movie.rating}</span>
          <span class="rating-outof">/ 10</span>
        </div>"""

    st.markdown(f"""
    <div class="movie-card">
      <div class="movie-title-block">
        <div class="movie-main-title">{movie.title}</div>
        {year_html}
      </div>

      <div class="info-row">
        {director_chip}
        {genres_html}
      </div>

      {rating_html}

      <hr class="inner-divider">

      <div class="section-label">Cast</div>
      <div class="cast-grid">{cast_html}</div>

      <hr class="inner-divider">

      <div class="section-label">Summary</div>
      <div class="summary-box">{movie.summary}</div>
    </div>
    """, unsafe_allow_html=True)


# ─── Input ────────────────────────────────────────────────────────────────────
paragraph = st.text_area(
    "Movie paragraph",
    placeholder="e.g. 'Interstellar (2014), directed by Christopher Nolan, stars Matthew McConaughey as Cooper...'",
    height=150,
    label_visibility="visible"
)

parse_btn = st.button("⬡  Parse Movie")


# ─── Extraction ───────────────────────────────────────────────────────────────
if parse_btn:
    if not paragraph.strip():
        st.markdown('<div class="err-box">⚠ Please enter a movie paragraph first.</div>', unsafe_allow_html=True)
    else:
        model, parser, prompt = load_chain()
        with st.spinner("Extracting…"):
            final_prompt = prompt.invoke({
                "paragraph": paragraph,
                "format_instructions": parser.get_format_instructions()
            })
            response = model.invoke(final_prompt)

        try:
            movie: Movie = parser.parse(response.content)
            render_movie_card(movie)
        except Exception as e:
            st.markdown(f'<div class="err-box">⚠ Could not parse structured output.<br><small>{e}</small></div>', unsafe_allow_html=True)
            with st.expander("Raw model output"):
                st.text(response.content)

        with st.expander("Parsed JSON"):
            try:
                st.json(json.loads(response.content))
            except Exception:
                st.text(response.content)
