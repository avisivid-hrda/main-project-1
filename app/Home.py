import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from sklearn.linear_model import LinearRegression

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Financial Power and Success in Football",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.image("../assets/banner.png", use_container_width=True)

# ── Theme / CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');

/* ── Global background gradient ── */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1b3e 40%, #0b2d7a 75%, #1246c4 100%) !important;
    font-family: 'Inter', sans-serif !important;
    color: #ffffff !important;
}
[data-testid="stHeader"] { background: transparent !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07101f 0%, #0a1a3a 100%) !important;
    border-right: 1px solid rgba(99,179,255,0.15) !important;
}
[data-testid="stSidebar"] * { color: #c8d8f0 !important; }
[data-testid="stSidebarNavLink"] {
    border-radius: 10px !important;
    margin: 2px 8px !important;
    transition: background 0.2s !important;
}
[data-testid="stSidebarNavLink"]:hover,
[data-testid="stSidebarNavLink"][aria-selected="true"] {
    background: linear-gradient(90deg, rgba(0,198,180,0.25), rgba(18,70,196,0.35)) !important;
    color: #00e5cc !important;
}

/* ── Main text ── */
h1, h2, h3, h4, h5, h6, p, li, span, label, div {
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Section label (small caps accent) ── */
.section-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    background: linear-gradient(90deg, #00e5cc, #4da6ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
}

/* ── Page title ── */
.page-title {
    font-size: 2.6rem;
    font-weight: 900;
    letter-spacing: -0.01em;
    line-height: 1.1;
    color: #ffffff !important;
    margin-bottom: 6px;
}
.page-subtitle {
    font-size: 1rem;
    color: rgba(200,216,240,0.75) !important;
    margin-bottom: 32px;
}

/* ── KPI cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin: 24px 0;
}
.kpi-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(99,179,255,0.18);
    border-radius: 16px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);
    transition: transform 0.2s, border-color 0.2s;
}
.kpi-card:hover {
    transform: translateY(-2px);
    border-color: rgba(0,229,204,0.4);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent, linear-gradient(90deg,#00e5cc,#4da6ff));
    border-radius: 16px 16px 0 0;
}
.kpi-icon { font-size: 1.5rem; margin-bottom: 8px; }
.kpi-label {
    font-size: 0.78rem !important;
    color: rgba(200,216,240,0.65) !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
    margin-bottom: 4px;
}
.kpi-value {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    line-height: 1;
}

/* ── Insight box ── */
.insight-box {
    background: rgba(0,229,204,0.07);
    border-left: 3px solid #00e5cc;
    border-radius: 0 12px 12px 0;
    padding: 14px 18px;
    margin: 12px 0;
    font-size: 0.92rem;
    color: rgba(220,235,255,0.9) !important;
}

/* ── Flourish placeholder ── */
.flourish-placeholder {
    background: rgba(255,255,255,0.03);
    border: 2px dashed rgba(99,179,255,0.3);
    border-radius: 16px;
    padding: 28px;
    text-align: center;
    color: rgba(200,216,240,0.5) !important;
    font-size: 0.88rem;
}
.flourish-placeholder b { color: #4da6ff !important; }

/* ── Divider ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,179,255,0.3), transparent);
    margin: 32px 0;
}

/* ── Chart container ── */
.chart-container {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(99,179,255,0.12);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
}

/* ── Plotly transparent bg ── */
.js-plotly-plot .plotly .main-svg { background: transparent !important; }

/* ── Selectbox / filters ── */
[data-testid="stSelectbox"] > div, [data-testid="stMultiSelect"] > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(99,179,255,0.2) !important;
    border-radius: 10px !important;
    color: #fff !important;
}

/* ── Metric override ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(99,179,255,0.18);
    border-radius: 14px;
    padding: 16px;
}
[data-testid="stMetricValue"] { color: #ffffff !important; font-weight: 800 !important; }
[data-testid="stMetricLabel"] { color: rgba(200,216,240,0.65) !important; }

/* ── Table ── */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }

/* ── Sidebar logo area ── */
.sidebar-logo {
    text-align: center;
    padding: 24px 16px 16px 16px;
    border-bottom: 1px solid rgba(99,179,255,0.12);
    margin-bottom: 8px;
}
.sidebar-logo-title {
    font-size: 1.1rem;
    font-weight: 800;
    background: linear-gradient(90deg, #00e5cc, #4da6ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.sidebar-logo-sub {
    font-size: 0.7rem;
    color: rgba(200,216,240,0.45) !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

# ── Plotly template ──────────────────────────────────────────────────────────
PLOTLY_TEMPLATE = dict(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(family="Inter", color="#c8d8f0"),
        title=dict(font=dict(color="#ffffff", size=16, family="Inter")),
        xaxis=dict(gridcolor="rgba(99,179,255,0.1)", linecolor="rgba(99,179,255,0.2)", tickcolor="rgba(99,179,255,0.3)"),
        yaxis=dict(gridcolor="rgba(99,179,255,0.1)", linecolor="rgba(99,179,255,0.2)", tickcolor="rgba(99,179,255,0.3)"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#c8d8f0")),
        colorway=["#00e5cc","#4da6ff","#ff6b9d","#f7c36a","#a78bfa","#34d399"],
    )
)

LEAGUE_COLORS = {
    "premier-league": "#00e5cc",
    "laliga":         "#4da6ff",
    "serie-a":        "#ff6b9d",
    "bundesliga":     "#f7c36a",
    "ligue-1":        "#a78bfa",
}
LEAGUE_LABELS = {
    "premier-league": "Premier League 🇬🇧",
    "laliga":         "La Liga 🇪🇸",
    "serie-a":        "Serie A 🇮🇹",
    "bundesliga":     "Bundesliga 🇩🇪",
    "ligue-1":        "Ligue 1 🇫🇷",
}

# ── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("../data/final/master_football_engineered.csv")
    df["spending_m"] = df["transfer_spending"] / 1e6
    df["svalue_m"]   = df["squad_market_value"] / 1e6
    df["league_label"] = df["league"].map(LEAGUE_LABELS)
    return df

df = load_data()

# ── Helpers ──────────────────────────────────────────────────────────────────
def section_header(label, title, subtitle=""):
    st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-title">⚽ {title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)

def insight(text):
    st.markdown(f'<div class="insight-box">💡 {text}</div>', unsafe_allow_html=True)

def divider():
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

def flourish_embed(url, height=500, caption=""):
    if url.startswith("PLACEHOLDER"):
        st.markdown(f"""
        <div class="flourish-placeholder">
            <b>📊 Flourish Chart Placeholder</b><br><br>
            Replace with your Flourish embed URL:<br>
            <code style="color:#00e5cc;background:rgba(0,229,204,0.1);padding:4px 8px;border-radius:6px;">{url}</code>
            {f'<br><br><em>{caption}</em>' if caption else ''}
        </div>""", unsafe_allow_html=True)
    else:
        st.components.v1.iframe(url, height=height, scrolling=False)

def apply_template(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(family="Inter", color="#c8d8f0", size=12),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#c8d8f0")),
        xaxis=dict(gridcolor="rgba(99,179,255,0.1)", linecolor="rgba(99,179,255,0.2)"),
        yaxis=dict(gridcolor="rgba(99,179,255,0.1)", linecolor="rgba(99,179,255,0.2)"),
        margin=dict(t=40, b=40, l=40, r=40),
    )
    return fig

# ── Sidebar navigation ────────────────────────────────────────────────────────
with st.sidebar:
    pages = {
        "Home":                    "home",
        "Financial Overview":      "financial",
        "Finance vs Performance":  "performance",
        "Efficiency Analysis":     "efficiency",
        "Overperformers":          "residuals",
        "Titles, Top 4 & Relegation": "outcomes",
    }
    selected = st.radio("", list(pages.keys()), label_visibility="collapsed")
    page = pages[selected]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "home":

    # Hero banner
    st.markdown("""
    <div style="
        background: linear-gradient(135deg,rgba(18,70,196,0.6),rgba(0,229,204,0.2));
        border:1px solid rgba(99,179,255,0.2);
        border-radius:20px;
        padding:48px 40px 40px 40px;
        margin-bottom:28px;
        position:relative;
        overflow:hidden;
    ">
        <div style="font-size:3.5rem;font-weight:900;letter-spacing:-0.02em;line-height:1;color:#fff;margin-bottom:16px;">
            THE PRICE OF<br>VICTORY
        </div>
        <div style="display:inline-block;background:linear-gradient(90deg,#00e5cc,#4da6ff);
            border-radius:8px;padding:10px 20px;font-weight:700;font-size:1rem;color:#0a0e1a;">
            Does Financial Power Drive Success in European Football?
        </div>
    """, unsafe_allow_html=True)

    # KPI Cards
    st.markdown("""
    <div class="kpi-grid">
        <div class="kpi-card" style="--accent:linear-gradient(90deg,#00e5cc,#4da6ff)">
            <div class="kpi-icon">🏟️</div>
            <div class="kpi-label">Total Clubs</div>
            <div class="kpi-value">160</div>
        </div>
        <div class="kpi-card" style="--accent:linear-gradient(90deg,#4da6ff,#a78bfa)">
            <div class="kpi-icon">🗓️</div>
            <div class="kpi-label">Seasons Covered</div>
            <div class="kpi-value">10</div>
        </div>
        <div class="kpi-card" style="--accent:linear-gradient(90deg,#a78bfa,#ff6b9d)">
            <div class="kpi-icon">🌍</div>
            <div class="kpi-label">Leagues Analysed</div>
            <div class="kpi-value">5</div>
        </div>
        <div class="kpi-card" style="--accent:linear-gradient(90deg,#f7c36a,#00e5cc)">
            <div class="kpi-icon">💰</div>
            <div class="kpi-label">Avg Squad Value</div>
            <div class="kpi-value">€599.5M</div>
        </div>
        <div class="kpi-card" style="--accent:linear-gradient(90deg,#ff6b9d,#f7c36a)">
            <div class="kpi-icon">📈</div>
            <div class="kpi-label">Avg Transfer Spend</div>
            <div class="kpi-value">€39.0M</div>
        </div>
        <div class="kpi-card" style="--accent:linear-gradient(90deg,#34d399,#4da6ff)">
            <div class="kpi-icon">📊</div>
            <div class="kpi-label">Total Records</div>
            <div class="kpi-value">978</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    divider()

    # Central research question
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
        <div style="font-size:0.72rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;
            background:linear-gradient(90deg,#00e5cc,#4da6ff);-webkit-background-clip:text;
            -webkit-text-fill-color:transparent;background-clip:text;margin-bottom:8px;">
            The Research Question
        </div>
        <div style="font-size:1.7rem;font-weight:800;line-height:1.25;color:#fff;margin-bottom:16px;">
            Does spending more money<br>guarantee winning more games?
        </div>
        <p style="color:rgba(200,216,240,0.75);font-size:0.95rem;line-height:1.7;">
            This project analyses a decade of financial and performance data across Europe's top 5 leagues —
            the Premier League, La Liga, Serie A, Bundesliga, and Ligue 1 — to understand how squad value
            and transfer spending relate to actual on-pitch outcomes.
        </p>
        <p style="color:rgba(200,216,240,0.75);font-size:0.95rem;line-height:1.7;">
            We go beyond simple correlations to identify which clubs punch above their financial weight,
            which ones waste fortunes, and how the relationship between money and success varies across
            different footballing cultures.
        </p>
        """, unsafe_allow_html=True)

    with col2:
        # Mini quick-stats
        st.markdown("""
        <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(99,179,255,0.18);
            border-radius:16px;padding:24px;">
            <div style="font-size:0.72rem;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;
                color:#00e5cc;margin-bottom:16px;">Key Findings Preview</div>
        """, unsafe_allow_html=True)

        findings = [
            ("🇬🇧", "Premier League spends <b>3× more</b> than Bundesliga on average"),
            ("📉", "Squad value predicts points better than transfer spend"),
            ("⚡", "30% of titles won by the <b>single highest spender</b>"),
            ("🦁", "Leicester City & Monaco — the great overperformers"),
            ("💸", "Chelsea 22/23: worst ROI — €574M for 44 points"),
            ("🕌", "Middle-East owned clubs initially overperform, then plateau"),
        ]
        for icon, text in findings:
            st.markdown(f"""
            <div style="display:flex;gap:12px;align-items:flex-start;margin-bottom:12px;">
                <span style="font-size:1.1rem;">{icon}</span>
                <span style="font-size:0.85rem;color:rgba(200,216,240,0.8);">{text}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    divider()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — FINANCIAL OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
elif page == "financial":
    section_header("Financial Overview", "Financial Landscape",
                   "How money is distributed across clubs, leagues and time.")

    # Flourish: Racing bar chart — squad value over time
    st.markdown("#### 📊 Squad Value Growth Over Time (Interactive — Flourish)")
    st.markdown('<div class="insight-box">💡 Replace the URL below with your Flourish Racing Bar Chart embed link. Recommended chart type: <b>Bar Chart Race</b> on flourish.studio</div>', unsafe_allow_html=True)
    flourish_embed(
        "PLACEHOLDER: https://flo.uri.sh/visualisation/YOUR_ID/embed",
        height=520,
        caption="Recommended: Flourish Bar Chart Race — Average Squad Value by League, 2014–2024"
    )

    divider()

    # Distribution charts
    st.markdown("#### Distribution of Squad Market Value & Transfer Spending")
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.histogram(df, x="svalue_m", nbins=40, color_discrete_sequence=["#4da6ff"],
                            labels={"svalue_m": "Squad Value (€M)"}, title="Squad Market Value Distribution")
        fig1.update_traces(opacity=0.8)
        apply_template(fig1)
        st.plotly_chart(fig1, use_container_width=True)
        insight("61% of clubs are worth under €500M. A small elite hold disproportionate value.")

    with col2:
        fig2 = px.histogram(df[df["spending_m"]>0], x="spending_m", nbins=40,
                            color_discrete_sequence=["#00e5cc"],
                            labels={"spending_m": "Transfer Spending (€M)"}, title="Transfer Spending Distribution")
        fig2.update_traces(opacity=0.8)
        apply_template(fig2)
        st.plotly_chart(fig2, use_container_width=True)
        insight("~90% of clubs spend under €100M. A handful of mega-spenders skew the distribution.")

    divider()

    # Box plots by league
    st.markdown("#### Spending & Squad Value by League")

    tab1, tab2 = st.tabs(["💰 Transfer Spending", "🏟️ Squad Value"])
    with tab1:
        fig3 = px.box(df, x="league_label", y="spending_m", color="league",
                      color_discrete_map={v: LEAGUE_COLORS[k] for k,v in LEAGUE_LABELS.items()},
                      labels={"spending_m":"Transfer Spend (€M)", "league_label":"League"},
                      title="Transfer Spending Distribution by League")
        apply_template(fig3)
        fig3.update_layout(showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)
        insight("The Premier League spends over 3× the Bundesliga on average. Ligue 1 shows extreme inequality driven by PSG.")

    with tab2:
        fig4 = px.box(df, x="league_label", y="svalue_m", color="league",
                      color_discrete_map={v: LEAGUE_COLORS[k] for k,v in LEAGUE_LABELS.items()},
                      labels={"svalue_m":"Squad Value (€M)", "league_label":"League"},
                      title="Squad Value Distribution by League")
        apply_template(fig4)
        fig4.update_layout(showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)
        insight("Premier League squads are worth nearly 2× La Liga on average, reflecting their TV revenue dominance.")

    divider()

    # Time trend
    st.markdown("#### Financial Growth Over Time")
    metric_choice = st.selectbox("Select metric", ["Squad Value (€M)", "Transfer Spending (€M)"])
    col_map = {"Squad Value (€M)": "svalue_m", "Transfer Spending (€M)": "spending_m"}
    col = col_map[metric_choice]

    trend = df.groupby(["year","league"])[col].mean().reset_index()
    trend["league_label"] = trend["league"].map(LEAGUE_LABELS)

    fig5 = px.line(trend, x="year", y=col, color="league",
                   color_discrete_map=LEAGUE_COLORS,
                   labels={"year":"Season Start Year", col: metric_choice},
                   title=f"Average {metric_choice} by League Over Time",
                   markers=True)
    apply_template(fig5)
    fig5.update_traces(line_width=2.5)
    st.plotly_chart(fig5, use_container_width=True)
    insight("Squad values have inflated 2–3× across all leagues since 2014. The Premier League gap has widened every season.")

    divider()

    # Financial inequality
    st.markdown("#### Financial Inequality (Coefficient of Variation)")
    cv = (df.groupby("league")["transfer_spending"].std() /
          df.groupby("league")["transfer_spending"].mean()).reset_index()
    cv.columns = ["league","cv"]
    cv = cv.sort_values("cv", ascending=True)
    cv["label"] = cv["league"].map(LEAGUE_LABELS)
    cv["color"] = cv["league"].map(LEAGUE_COLORS)

    fig6 = go.Figure(go.Bar(
        x=cv["cv"].round(2), y=cv["label"], orientation="h",
        marker_color=cv["color"].tolist(),
        text=cv["cv"].round(2), textposition="outside",
    ))
    fig6.update_layout(
        title="Transfer Spending Inequality by League (Higher = More Unequal)",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.03)",
        font=dict(family="Inter", color="#c8d8f0"),
        xaxis=dict(gridcolor="rgba(99,179,255,0.1)", title="Coefficient of Variation"),
        yaxis=dict(linecolor="rgba(99,179,255,0.2)"),
        margin=dict(t=40,b=20,l=20,r=60), height=320, showlegend=False,
    )
    st.plotly_chart(fig6, use_container_width=True)
    insight("Ligue 1 is the most financially unequal league — PSG's dominance distorts the entire competition. The Premier League is ironically the most equal despite its size.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — FINANCE vs PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "performance":
    section_header("Finance vs Performance", "Financial Power & On-Pitch Results",
                   "Explore how financial strength relates to on-pitch outcomes across leagues, seasons, and clubs.")

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        league_sel = st.selectbox("League", ["All"] + list(LEAGUE_LABELS.values()))
    with col2:
        season_sel = st.selectbox("Season", ["All"] + sorted(df["season"].unique()))
    with col3:
        ownership = st.selectbox("Ownership", ["All", "Middle East Owned", "Other"])

    dff = df.copy()
    if league_sel != "All": dff = dff[dff["league_label"] == league_sel]
    if season_sel != "All": dff = dff[dff["season"] == season_sel]
    if ownership == "Middle East Owned": dff = dff[dff["middle_east_owned"]==1]
    elif ownership == "Other": dff = dff[dff["middle_east_owned"]==0]

    # Flourish scatter
    st.markdown("#### 🌐 Interactive Scatter (Flourish — Squad Value vs Points)")
    flourish_embed(
        "PLACEHOLDER: https://flo.uri.sh/visualisation/YOUR_SCATTER_ID/embed",
        height=540,
        caption="Recommended: Flourish Scatter Plot — Squad Market Value (x) vs Points (y), coloured by League"
    )

    divider()

    # Plotly scatter fallback (interactive)
    st.markdown("#### Squad Value vs Points — Explore the Data")
    col_x = st.selectbox("X-axis", ["svalue_m","spending_m"], format_func=lambda x: "Squad Value (€M)" if x=="svalue_m" else "Transfer Spending (€M)")
    col_y = st.selectbox("Y-axis", ["points","wins","goal_difference","position"],
                         format_func=lambda x: {"points":"Points","wins":"Wins","goal_difference":"Goal Difference","position":"League Position"}[x])
    color_by = st.selectbox("Colour by", ["league","title_won","top4_finish","middle_east_owned"])

    fig_sc = px.scatter(dff, x=col_x, y=col_y,
                        color=color_by if color_by=="league" else None,
                        color_discrete_map=LEAGUE_COLORS if color_by=="league" else None,
                        color_continuous_scale="teal" if color_by!="league" else None,
                        hover_data=["club_name","season","league"],
                        trendline="ols",
                        labels={col_x: "Squad Value (€M)" if col_x=="svalue_m" else "Transfer Spending (€M)",
                                col_y: col_y.replace("_"," ").title()},
                        title=f"{'Squad Value' if col_x=='svalue_m' else 'Transfer Spending'} vs {col_y.replace('_',' ').title()}")
    apply_template(fig_sc)
    fig_sc.update_traces(marker=dict(size=7, opacity=0.75))
    st.plotly_chart(fig_sc, use_container_width=True)

    divider()

    # Correlation heatmap
    st.markdown("#### Correlation Matrix — Finance & Performance")
    corr_cols = ["squad_market_value","transfer_spending","points","wins","goals_for","goal_difference","position"]
    corr = dff[corr_cols].corr().round(2)
    fig_heat = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.columns,
        colorscale=[[0,"#1246c4"],[0.5,"#0a0e1a"],[1,"#00e5cc"]],
        zmid=0, text=corr.values, texttemplate="%{text}",
        showscale=True,
    ))
    fig_heat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#c8d8f0"),
        margin=dict(t=20,b=20,l=20,r=20), height=420,
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    insight("Squad value has the strongest correlation with points (~0.63) and wins. Transfer spending alone is a weaker predictor (~0.44).")

    divider()

    # Correlation by league
    st.markdown("#### How Important is Finance in Each League?")
    corr_league = df.groupby("league").apply(
        lambda x: pd.Series({
            "Squad Value vs Points": x["squad_market_value"].corr(x["points"]).round(3),
            "Transfer Spend vs Points": x["transfer_spending"].corr(x["points"]).round(3),
        })
    ).reset_index()
    corr_league["label"] = corr_league["league"].map(LEAGUE_LABELS)
    corr_melt = corr_league.melt(id_vars=["league","label"], var_name="Metric", value_name="Correlation")

    fig_corr = px.bar(corr_melt, x="label", y="Correlation", color="Metric",
                      barmode="group",
                      color_discrete_sequence=["#00e5cc","#4da6ff"],
                      labels={"label":"League","Correlation":"Pearson Correlation"},
                      title="Correlation Between Finance and Points by League")
    apply_template(fig_corr)
    st.plotly_chart(fig_corr, use_container_width=True)
    insight("Serie A has the strongest squad-value-to-points link (0.74). Bundesliga shows the weakest — suggesting more competitive balance despite financial gaps.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — EFFICIENCY ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "efficiency":
    section_header("Efficiency Analysis", "Who Gets the Most From Their Money?",
                   "Identifying clubs that deliver exceptional value relative to their financial investment.")

    # Flourish: bump chart
    st.markdown("#### 📊 Points per €100M Squad Value — Season Rankings (Flourish)")
    flourish_embed(
        "PLACEHOLDER: https://flo.uri.sh/visualisation/YOUR_BUMP_CHART_ID/embed",
        height=500,
        caption="Recommended: Flourish Slope / Bump Chart — Efficiency ranking over seasons"
    )

    divider()

    metric = st.radio("Efficiency Metric", ["Points per €100M Squad Value", "Points per €10M Transfer Spend"], horizontal=True)

    if metric == "Points per €100M Squad Value":
        eff_df = df[df["squad_market_value"] >= 100_000_000].copy()
        eff_df["efficiency"] = eff_df["points"] / (eff_df["squad_market_value"] / 1e8)
        xlabel = "Points per €100M Squad Value"
    else:
        eff_df = df[df["transfer_spending"] >= 10_000_000].copy()
        eff_df["efficiency"] = eff_df["points"] / (eff_df["transfer_spending"] / 1e7)
        xlabel = "Points per €10M Transfer Spend"

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### 🏅 Top 15 Most Efficient Clubs (Season)")
        top_eff = eff_df.nlargest(15, "efficiency")[["club_name","league","season","points","efficiency"]].copy()
        top_eff["efficiency"] = top_eff["efficiency"].round(2)
        top_eff.columns = ["Club","League","Season","Points","Efficiency Score"]

        fig_top = go.Figure(go.Bar(
            x=top_eff["Efficiency Score"], y=top_eff["Club"] + " " + top_eff["Season"],
            orientation="h", marker_color="#00e5cc",
            text=top_eff["Efficiency Score"], textposition="outside",
        ))
        fig_top.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.03)",
            font=dict(family="Inter", color="#c8d8f0"),
            xaxis=dict(gridcolor="rgba(99,179,255,0.1)", title=xlabel),
            yaxis=dict(autorange="reversed"),
            margin=dict(t=10,b=20,l=20,r=60), height=500, showlegend=False,
        )
        st.plotly_chart(fig_top, use_container_width=True)

    with col2:
        st.markdown("##### ❌ 15 Least Efficient Clubs (Season)")
        bot_eff = eff_df.nsmallest(15, "efficiency")[["club_name","league","season","points","efficiency"]].copy()
        bot_eff["efficiency"] = bot_eff["efficiency"].round(2)
        bot_eff.columns = ["Club","League","Season","Points","Efficiency Score"]

        fig_bot = go.Figure(go.Bar(
            x=bot_eff["Efficiency Score"], y=bot_eff["Club"] + " " + bot_eff["Season"],
            orientation="h", marker_color="#ff6b9d",
            text=bot_eff["Efficiency Score"], textposition="outside",
        ))
        fig_bot.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.03)",
            font=dict(family="Inter", color="#c8d8f0"),
            xaxis=dict(gridcolor="rgba(99,179,255,0.1)", title=xlabel),
            yaxis=dict(autorange="reversed"),
            margin=dict(t=10,b=20,l=20,r=60), height=500, showlegend=False,
        )
        st.plotly_chart(fig_bot, use_container_width=True)

    divider()

    # Efficiency by league box
    st.markdown("#### Efficiency Distribution by League")
    fig_eff_box = px.box(eff_df, x="league_label", y="efficiency", color="league",
                         color_discrete_map={v: LEAGUE_COLORS[k] for k,v in LEAGUE_LABELS.items()},
                         labels={"efficiency": xlabel, "league_label": "League"},
                         title=f"{xlabel} — Distribution by League")
    apply_template(fig_eff_box)
    fig_eff_box.update_layout(showlegend=False)
    st.plotly_chart(fig_eff_box, use_container_width=True)
    insight("Smaller, well-organised clubs consistently outperform on efficiency. RB Leipzig and Sassuolo regularly appear as best-value clubs in their respective leagues.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — OVERPERFORMERS & RESIDUALS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "residuals":
    section_header("Overperformers & Underperformers", "Who Beats (and Busts) Financial Expectations?",
                   "Residual analysis — comparing actual points to what a club's squad value predicted.")

    # Compute residuals
    @st.cache_data
    def compute_residuals(df):
        d = df.copy()
        X = d[["squad_market_value"]].fillna(0)
        y = d["points"]
        model = LinearRegression().fit(X, y)
        d["predicted_points"] = model.predict(X).round(1)
        d["residual"] = (d["points"] - d["predicted_points"]).round(1)

        d2 = d[d["transfer_spending"] > 0].copy()
        X2 = d2[["transfer_spending"]]
        y2 = d2["points"]
        m2 = LinearRegression().fit(X2, y2)
        d2["pred_pts_spend"] = m2.predict(X2).round(1)
        d2["residual_spend"] = (d2["points"] - d2["pred_pts_spend"]).round(1)
        d = d.merge(d2[["club_id","year","pred_pts_spend","residual_spend"]], on=["club_id","year"], how="left")
        return d

    dres = compute_residuals(df)

    # Flourish
    st.markdown("#### 📊 Actual vs Expected Points — All Clubs (Flourish)")
    flourish_embed(
        "PLACEHOLDER: https://flo.uri.sh/visualisation/YOUR_RESIDUAL_CHART_ID/embed",
        height=520,
        caption="Recommended: Flourish Scatter or Connected Dot Plot — Actual vs Predicted points, coloured by residual direction"
    )

    divider()

    residual_basis = st.radio("Residual Basis", ["Squad Value", "Transfer Spending"], horizontal=True)

    if residual_basis == "Squad Value":
        res_col = "residual"
        sub = dres.dropna(subset=[res_col])
    else:
        res_col = "residual_spend"
        sub = dres.dropna(subset=[res_col])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### 🚀 Top 10 Overperformers")
        top_over = sub.nlargest(10, res_col)[["club_name","league","season","points","predicted_points" if residual_basis=="Squad Value" else "pred_pts_spend", res_col]].copy()
        top_over.columns = ["Club","League","Season","Actual Pts","Predicted Pts","Residual"]

        fig_ov = go.Figure(go.Bar(
            x=top_over["Residual"], y=top_over["Club"] + "\n" + top_over["Season"],
            orientation="h", marker_color="#00e5cc",
            text=top_over["Residual"].apply(lambda x: f"+{x}"), textposition="outside",
        ))
        fig_ov.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.03)",
            font=dict(family="Inter", color="#c8d8f0"),
            xaxis=dict(gridcolor="rgba(99,179,255,0.1)", title="Points above expectation"),
            yaxis=dict(autorange="reversed"),
            margin=dict(t=10,b=20,l=20,r=60), height=400, showlegend=False,
        )
        st.plotly_chart(fig_ov, use_container_width=True)

    with col2:
        st.markdown("##### 💸 Top 10 Underperformers")
        top_under = sub.nsmallest(10, res_col)[["club_name","league","season","points","predicted_points" if residual_basis=="Squad Value" else "pred_pts_spend", res_col]].copy()
        top_under.columns = ["Club","League","Season","Actual Pts","Predicted Pts","Residual"]

        fig_un = go.Figure(go.Bar(
            x=top_under["Residual"], y=top_under["Club"] + "\n" + top_under["Season"],
            orientation="h", marker_color="#ff6b9d",
            text=top_under["Residual"], textposition="outside",
        ))
        fig_un.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.03)",
            font=dict(family="Inter", color="#c8d8f0"),
            xaxis=dict(gridcolor="rgba(99,179,255,0.1)", title="Points below expectation"),
            yaxis=dict(autorange="reversed"),
            margin=dict(t=10,b=20,l=20,r=60), height=400, showlegend=False,
        )
        st.plotly_chart(fig_un, use_container_width=True)

    col1i, col2i = st.columns(2)
    with col1i:
        insight("Monaco 2016/17 — won Ligue 1 with 95 points despite a modest squad value. The Mbappé/Lemar generation before the selloff.")
    with col2i:
        insight("Chelsea 2022/23 — worst underperformer: €574M spent, only 44 pts. The most extreme waste of resources in the entire dataset.")

    divider()

    # Middle East Ownership
    st.markdown("#### 🕌 Middle East Owned Clubs — Performance vs Expectations Over Time")
    me = dres[dres["middle_east_owned"] == 1].sort_values("year")

    fig_me = px.line(me, x="year", y=res_col, color="club_name",
                     color_discrete_sequence=["#00e5cc","#4da6ff","#f7c36a"],
                     markers=True,
                     labels={"year":"Year", res_col:"Residual (Actual − Predicted Points)", "club_name":"Club"},
                     title="Residual Points — Middle East Owned Clubs")
    apply_template(fig_me)
    fig_me.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.3)", annotation_text="Expected")
    fig_me.update_traces(line_width=2.5)
    st.plotly_chart(fig_me, use_container_width=True)
    insight("Man City and PSG initially overperformed heavily. As their squads became the most expensive in their leagues, their residuals converged to zero — great performance now simply meets inflated expectations.")

    divider()

    # Residual distribution
    st.markdown("#### Residual Distribution — How Well Does Squad Value Predict Points?")
    fig_dist = px.histogram(sub, x="residual", nbins=40, color_discrete_sequence=["#4da6ff"],
                            labels={"residual":"Residual (Actual − Predicted Points)"})
    fig_dist.add_vline(x=0, line_dash="dash", line_color="#00e5cc", annotation_text="0 (perfect prediction)")
    apply_template(fig_dist)
    st.plotly_chart(fig_dist, use_container_width=True)
    insight("Most prediction errors cluster near zero — the model is generally balanced. But errors can still be ±30 points, proving football isn't just about money.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — TITLES, TOP 4, RELEGATION
# ══════════════════════════════════════════════════════════════════════════════
elif page == "outcomes":
    section_header("Titles, Top 4 & Relegation", "Does Money Buy Trophies?",
                   "How financial strength maps to the three most critical competitive outcomes.")

    # Flourish
    st.markdown("#### 📊 Title Winners by Spending Rank — All Seasons (Flourish)")
    flourish_embed(
        "PLACEHOLDER: https://flo.uri.sh/visualisation/YOUR_TITLES_CHART_ID/embed",
        height=480,
        caption="Recommended: Flourish Pie / Donut or Sankey — Title winners broken down by spending rank bucket"
    )

    divider()

    outcome_tabs = st.tabs(["🏆 Title Winners", "⭐ Top 4 (UCL)", "⬇️ Relegation"])

    with outcome_tabs[0]:
        title_df = df[df["title_won"] == 1]
        spend_dist = title_df["spending_rank"].value_counts().reset_index()
        spend_dist.columns = ["Spending Rank","Count"]
        spend_dist = spend_dist.sort_values("Spending Rank")
        spend_dist["Pct"] = (spend_dist["Count"] / spend_dist["Count"].sum() * 100).round(1)
        spend_dist["Rank Group"] = spend_dist["Spending Rank"].apply(
            lambda x: "Rank 1" if x==1 else ("Top 3" if x<=3 else ("Top 6" if x<=6 else "7+"))
        )
        group_agg = spend_dist.groupby("Rank Group")[["Count","Pct"]].sum().reset_index()
        order = ["Rank 1","Top 3","Top 6","7+"]
        group_agg["Rank Group"] = pd.Categorical(group_agg["Rank Group"], categories=order, ordered=True)
        group_agg = group_agg.sort_values("Rank Group")

        col1, col2 = st.columns(2)
        with col1:
            fig_pie = go.Figure(go.Pie(
                labels=group_agg["Rank Group"], values=group_agg["Count"],
                marker_colors=["#00e5cc","#4da6ff","#a78bfa","#f7c36a"],
                hole=0.55,
                textinfo="label+percent",
                textfont=dict(color="#ffffff", size=13),
            ))
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter",color="#c8d8f0"),
                title="Title Wins by Spending Rank Group",
                showlegend=False, height=380, margin=dict(t=40,b=20),
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            st.markdown("##### Title Win Rate by Spending Rank")
            win_rate = df.groupby("spending_rank").agg(
                titles=("title_won","sum"),
                total=("title_won","count"),
            ).reset_index()
            win_rate["win_rate"] = (win_rate["titles"] / win_rate["total"] * 100).round(1)
            win_rate = win_rate[win_rate["spending_rank"] <= 10]

            fig_wr = go.Figure(go.Bar(
                x=win_rate["spending_rank"], y=win_rate["win_rate"],
                marker_color=["#00e5cc" if r<=3 else "#4da6ff" if r<=6 else "#a78bfa" for r in win_rate["spending_rank"]],
                text=win_rate["win_rate"].apply(lambda x: f"{x}%"), textposition="outside",
            ))
            fig_wr.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.03)",
                font=dict(family="Inter",color="#c8d8f0"),
                xaxis=dict(title="Spending Rank", dtick=1, gridcolor="rgba(99,179,255,0.1)"),
                yaxis=dict(title="Title Win Rate (%)", gridcolor="rgba(99,179,255,0.1)"),
                margin=dict(t=20,b=20,l=20,r=40), height=320, showlegend=False,
            )
            st.plotly_chart(fig_wr, use_container_width=True)

        insight("30% of all titles were won by the single highest spender — far above the 5% random chance baseline. Yet 70% of titles were won outside the top spender, proving money helps but doesn't guarantee.")

    with outcome_tabs[1]:
        df["spending_bucket"] = pd.cut(df["spending_rank"],
            bins=[0,3,6,10,15,25], labels=["Top 3","4–6","7–10","11–15","16+"])
        df["value_bucket"] = pd.cut(df["value_rank"],
            bins=[0,3,6,10,15,25], labels=["Top 3","4–6","7–10","11–15","16+"])

        col1, col2 = st.columns(2)
        with col1:
            top4_spend = df.groupby("spending_bucket", observed=True)["top4_finish"].mean().reset_index()
            top4_spend["rate"] = (top4_spend["top4_finish"] * 100).round(1)
            fig_t4s = px.bar(top4_spend, x="spending_bucket", y="rate",
                             color="rate", color_continuous_scale=[[0,"#1246c4"],[1,"#00e5cc"]],
                             labels={"spending_bucket":"Spending Rank Bucket","rate":"Top 4 Rate (%)"},
                             title="Top 4 Finish Rate by Transfer Spending Rank")
            apply_template(fig_t4s)
            fig_t4s.update_layout(showlegend=False, coloraxis_showscale=False)
            fig_t4s.update_traces(text=top4_spend["rate"].apply(lambda x: f"{x}%"), textposition="outside")
            st.plotly_chart(fig_t4s, use_container_width=True)

        with col2:
            top4_val = df.groupby("value_bucket", observed=True)["top4_finish"].mean().reset_index()
            top4_val["rate"] = (top4_val["top4_finish"] * 100).round(1)
            fig_t4v = px.bar(top4_val, x="value_bucket", y="rate",
                             color="rate", color_continuous_scale=[[0,"#1246c4"],[1,"#4da6ff"]],
                             labels={"value_bucket":"Squad Value Rank Bucket","rate":"Top 4 Rate (%)"},
                             title="Top 4 Finish Rate by Squad Value Rank")
            apply_template(fig_t4v)
            fig_t4v.update_layout(showlegend=False, coloraxis_showscale=False)
            fig_t4v.update_traces(text=top4_val["rate"].apply(lambda x: f"{x}%"), textposition="outside")
            st.plotly_chart(fig_t4v, use_container_width=True)

        insight("Top 3 spenders finish in the Champions League places 60–70% of the time. Beyond the top 6, the drop-off is steep — mid-table spenders rarely qualify.")

    with outcome_tabs[2]:
        col1, col2 = st.columns(2)
        with col1:
            rel_spend = df.groupby("spending_bucket", observed=True)["relegated"].mean().reset_index()
            rel_spend["rate"] = (rel_spend["relegated"] * 100).round(1)
            fig_rs = px.bar(rel_spend, x="spending_bucket", y="rate",
                            color="rate", color_continuous_scale=[[0,"#1246c4"],[1,"#ff6b9d"]],
                            labels={"spending_bucket":"Spending Rank Bucket","rate":"Relegation Rate (%)"},
                            title="Relegation Rate by Transfer Spending Rank")
            apply_template(fig_rs)
            fig_rs.update_layout(showlegend=False, coloraxis_showscale=False)
            fig_rs.update_traces(text=rel_spend["rate"].apply(lambda x: f"{x}%"), textposition="outside")
            st.plotly_chart(fig_rs, use_container_width=True)

        with col2:
            rel_val = df.groupby("value_bucket", observed=True)["relegated"].mean().reset_index()
            rel_val["rate"] = (rel_val["relegated"] * 100).round(1)
            fig_rv = px.bar(rel_val, x="value_bucket", y="rate",
                            color="rate", color_continuous_scale=[[0,"#1246c4"],[1,"#f7c36a"]],
                            labels={"value_bucket":"Squad Value Rank Bucket","rate":"Relegation Rate (%)"},
                            title="Relegation Rate by Squad Value Rank")
            apply_template(fig_rv)
            fig_rv.update_layout(showlegend=False, coloraxis_showscale=False)
            fig_rv.update_traces(text=rel_val["rate"].apply(lambda x: f"{x}%"), textposition="outside")
            st.plotly_chart(fig_rv, use_container_width=True)

        insight("No club ranked in the top 3 by squad value has ever been relegated in this dataset. Bottom 5 spenders face dramatically higher relegation risk — financial weakness directly threatens survival.")

    divider()

    # League-level title concentration
    st.markdown("#### Title Concentration — Do the Same Clubs Always Win?")
    title_clubs = df[df["title_won"]==1].groupby(["league","club_name"]).size().reset_index(name="titles")
    title_clubs["league_label"] = title_clubs["league"].map(LEAGUE_LABELS)
    title_clubs = title_clubs.sort_values(["league","titles"], ascending=[True, False])

    fig_conc = px.bar(title_clubs, x="titles", y="club_name", color="league",
                      color_discrete_map=LEAGUE_COLORS,
                      facet_col="league_label", facet_col_wrap=3,
                      labels={"titles":"Titles Won","club_name":"Club"},
                      title="Title Distribution by Club and League (2014–2024)")
    apply_template(fig_conc)
    fig_conc.update_layout(showlegend=False, height=520)
    fig_conc.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    st.plotly_chart(fig_conc, use_container_width=True)
    insight("Bundesliga and Ligue 1 show extreme title concentration — Bayern and PSG dominated for most of the decade. The Premier League saw the most variety, with 5 different champions.")