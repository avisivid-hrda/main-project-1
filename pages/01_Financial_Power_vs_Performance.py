import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Financial vs Performance",
    page_icon="⚽",
    layout="wide",
)

# ---------------------------
# Data loading
# ---------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/final/master_football_engineered.csv")

df = load_data()

# ---------------------------
# Styling
# ---------------------------
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0E1117;
    }

    .stApp {
        background-color: #0E1117;
        color: #F5F5F5;
    }

    .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    section[data-testid="stSidebar"] {
        background-color: #0E1117;
    }

    section[data-testid="stSidebar"] * {
        color: #F5F5F5;
    }

    div[data-baseweb="select"] > div {
        background-color: #161B22 !important;
        color: #F5F5F5 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
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

    .section-label {
        margin-top: 0.5rem;
        font-size: 0.95rem;
        font-weight: 700;
        color: #F4C542;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.4rem;
    }

    .hero-title {
        margin-top: 0.2rem;
        font-size: 2.3rem;
        font-weight: 800;
        color: #F5F5F5;
        margin-bottom: 0.2rem;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #A9B1BD;
        margin-bottom: 1.8rem;
        max-width: 800px;
    }

    .panel {
        background: linear-gradient(180deg, #161B22 0%, #11161C 100%);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 18px;
        padding: 1rem 1rem;
        box-shadow: 0 4px 18px rgba(0,0,0,0.20);
        margin-bottom: 1rem;
    }

    label[data-testid="stWidgetLabel"] p {
    color: #F5F5F5 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Header
# ---------------------------
st.markdown('<div class="section-label">Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">⚽ Financial vs Performance</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="hero-subtitle">
        Explore how financial strength relates to on-pitch outcomes across leagues, seasons, and clubs.
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Sidebar filters
# ---------------------------
st.sidebar.header("Filters")

league_options = sorted(df["league"].dropna().unique())
season_options = sorted(df["season"].dropna().unique())

selected_league = st.sidebar.selectbox(
    "League",
    options=["All"] + league_options,
    index=0
)

selected_season = st.sidebar.selectbox(
    "Season",
    options=["All"] + season_options,
    index=0
)

club_pool = df.copy()
if selected_league != "All":
    club_pool = club_pool[club_pool["league"] == selected_league]
if selected_season != "All":
    club_pool = club_pool[club_pool["season"] == selected_season]

club_options = sorted(club_pool["club_name"].dropna().unique())

selected_club = st.sidebar.selectbox(
    "Club",
    options=["All"] + club_options,
    index=0
)

ownership_options = ["All", "Middle-East Owned", "Others"]
selected_ownership = st.sidebar.selectbox(
    "Ownership",
    options=ownership_options,
    index=0
)

selected_outcome = st.sidebar.selectbox(
    "Competition Outcome",
    options=["All", "Title Winners", "Top 4", "Relegated"],
    index=0
)

# ---------------------------
# Chart controls
# ---------------------------
metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    x_var = st.selectbox(
        "X-axis",
        options=["squad_market_value", "transfer_spending"],
        index=0
    )

with metric_col2:
    y_var = st.selectbox(
        "Y-axis",
        options=["points", "wins", "goals_for", "goal_difference"],
        index=0
    )

with metric_col3:
    color_var = st.selectbox(
        "Color by",
        options=["league", "middle_east_owned"],
        index=0
    )

show_regression = st.checkbox("Show regression line", value=True)

# ---------------------------
# Apply filters
# ---------------------------
filtered_df = df.copy()

if selected_league != "All":
    filtered_df = filtered_df[filtered_df["league"] == selected_league]

if selected_season != "All":
    filtered_df = filtered_df[filtered_df["season"] == selected_season]

if selected_club != "All":
    filtered_df = filtered_df[filtered_df["club_name"] == selected_club]

if selected_ownership == "Middle-East Owned":
    filtered_df = filtered_df[filtered_df["middle_east_owned"] == 1]
elif selected_ownership == "Others":
    filtered_df = filtered_df[filtered_df["middle_east_owned"] == 0]

if selected_outcome == "Title Winners":
    filtered_df = filtered_df[filtered_df["position"] == 1]
elif selected_outcome == "Top 4":
    filtered_df = filtered_df[filtered_df["position"] <= 4]
elif selected_outcome == "Relegated":
    filtered_df = filtered_df[filtered_df["relegated"] == 1]

plot_df = filtered_df.loc[:, [x_var, y_var, color_var, "club_name", "season", "league"]].copy()
plot_df = plot_df.loc[:, ~plot_df.columns.duplicated()].dropna()

# ---------------------------
# Scatter plot
# ---------------------------
fig = px.scatter(
    plot_df,
    x=x_var,
    y=y_var,
    color=color_var,
    hover_name="club_name",
    hover_data={
        "season": True,
        "league": True,
        x_var: ":,.0f",
        y_var: ":,.0f"
    },
    template="plotly_dark",
    opacity=0.8
)

if show_regression and len(plot_df) >= 2:
    x_vals = plot_df[x_var].astype(float).values
    y_vals = plot_df[y_var].astype(float).values
    slope, intercept = np.polyfit(x_vals, y_vals, 1)

    x_line = np.linspace(x_vals.min(), x_vals.max(), 100)
    y_line = slope * x_line + intercept

    fig.add_scatter(
        x=x_line,
        y=y_line,
        mode="lines",
        name="Regression line"
    )

fig.update_layout(
    height=600,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    font=dict(color="#F5F5F5"),
    xaxis=dict(
        title_font=dict(color="#F5F5F5"),
        tickfont=dict(color="#F5F5F5")
    ),
    yaxis=dict(
        title_font=dict(color="#F5F5F5"),
        tickfont=dict(color="#F5F5F5")
    ),
    legend=dict(
        font=dict(color="#F5F5F5"),
        title=dict(font=dict(color="#F5F5F5"))
    ),
    margin=dict(l=20, r=20, t=40, b=20)
)

fig.update_traces(marker=dict(size=10))

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Details table
# ---------------------------

display_df = filtered_df[
    ["club_name", "league", "season", "squad_market_value", "transfer_spending", "points", "wins", "position"]
].copy()

display_df = display_df.rename(columns={
    "club_name": "Club",
    "league": "League",
    "season": "Season",
    "squad_market_value": "Squad Value (€)",
    "transfer_spending": "Transfer Spending (€)",
    "points": "Points",
    "wins": "Wins",
    "position": "Position"
})

display_df["Squad Value (€)"] = display_df["Squad Value (€)"].map(lambda x: f"€{x:,.0f}")
display_df["Transfer Spending (€)"] = display_df["Transfer Spending (€)"].map(lambda x: f"€{x:,.0f}")

st.markdown("### Summary")
st.dataframe(display_df, use_container_width=True, hide_index=True)