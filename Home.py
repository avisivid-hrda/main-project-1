import streamlit as st
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "data/final/master_football_engineered.csv")

df = pd.read_csv(file_path)

st.set_page_config(
    page_title="Financial Power and Success in Football",
    page_icon="⚽",
    layout="wide",
)

# ---------------------------
# Data loading
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/final/master_football_engineered.csv")
    return df

df = load_data()

# ---------------------------
# Metrics
# ---------------------------
total_clubs = df["club_name"].nunique()
seasons_covered = df["season"].nunique()
leagues_covered = df["league"].nunique()
avg_squad_value = df["squad_market_value"].mean()
avg_transfer_spending = df["transfer_spending"].mean() 

# ---------------------------
# Formatting helpers
# ---------------------------
def format_currency_millions(value):
    return f"€{value/1e6:,.1f}M"

def format_number(value):
    return f"{value:,.1f}"

# ---------------------------
# Custom styling
# ---------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #F5F5F5;
    }

    .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        color: #F5F5F5;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #A9B1BD;
        margin-bottom: 2rem;
        max-width: 780px;
    }

    .section-label {
        font-size: 0.95rem;
        font-weight: 700;
        color: #F4C542;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.4rem;
    }

    .metric-card {
        background: linear-gradient(180deg, #161B22 0%, #11161C 100%);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 18px;
        padding: 1.1rem 1rem;
        min-height: 135px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.20);
    }

    .metric-icon {
        font-size: 1.3rem;
        margin-bottom: 0.6rem;
    }

    .metric-label {
        font-size: 0.92rem;
        color: #A9B1BD;
        margin-bottom: 0.35rem;
    }

    .metric-value {
        font-size: 1.7rem;
        font-weight: 800;
        color: #F5F5F5;
        line-height: 1.1;
    }

    .metric-accent-red {
        border-left: 4px solid #D72638;
    }

    .metric-accent-yellow {
        border-left: 4px solid #F4C542;
    }

    .metric-accent-green {
        border-left: 4px solid #2FA36B;
    }

    .info-panel {
        margin-top: 2rem;
        background: #121820;
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 18px;
        padding: 1.2rem 1.2rem;
    }

    .info-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #F5F5F5;
        margin-bottom: 0.6rem;
    }

    .info-text {
        color: #A9B1BD;
        font-size: 0.98rem;
        line-height: 1.6;
    }
            
    section[data-testid="stSidebar"] {
    background-color: #0E1117;
    }

    section[data-testid="stSidebar"] * {
    color: #F5F5F5;
    }
            
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #0E1117;
    }
            
    div[data-baseweb="select"] > div {
    background-color: #161B22 !important;
    color: #F5F5F5 !important;
    }

    div[data-baseweb="select"] input {
    color: #F5F5F5 !important;
    -webkit-text-fill-color: #F5F5F5 !important;
    }
            
    div[data-baseweb="select"] svg {
    fill: #F5F5F5 !important;
    color: #F5F5F5 !important;
    opacity: 1 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Header
# ---------------------------
st.markdown('<div class="section-label">Overview</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">⚽ Financial Power and Success in Football</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="hero-subtitle">
        Explore club performance, financial strength, and league-level patterns across Europe’s top 5 leagues.
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Top metrics
# ---------------------------
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card metric-accent-red">
        <div class="metric-icon">🏟️</div>
        <div class="metric-label">Total Clubs</div>
        <div class="metric-value">{total_clubs}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card metric-accent-yellow">
        <div class="metric-icon">📅</div>
        <div class="metric-label">Seasons Covered</div>
        <div class="metric-value">{seasons_covered}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card metric-accent-green">
        <div class="metric-icon">🌍</div>
        <div class="metric-label">Leagues Covered</div>
        <div class="metric-value">{leagues_covered}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card metric-accent-green">
        <div class="metric-icon">💶</div>
        <div class="metric-label">Average Squad Value</div>
        <div class="metric-value">{format_currency_millions(avg_squad_value)}</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card metric-accent-red">
        <div class="metric-icon">📈</div>
        <div class="metric-label">Average Transfer Spending</div>
        <div class="metric-value">{format_currency_millions(avg_transfer_spending)}</div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.empty()

# ---------------------------
# Optional intro panel
# ---------------------------
st.markdown("""
<div class="info-panel">
    <div class="info-title">What this app will show</div>
    <div class="info-text">
        The full app will examine how squad market value and transfer spending relate to football outcomes,
        which clubs are most efficient with their resources, and which teams overperform relative to financial expectations.
    </div>
</div>
""", unsafe_allow_html=True)