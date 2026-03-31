import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import (inject_css, load_data, section_header, insight, divider,
                   flourish_embed, apply_template, LEAGUE_COLORS, LEAGUE_LABELS)

st.set_page_config(page_title="Finance vs Performance", page_icon="⚽", layout="wide")
inject_css()

df = load_data()

section_header("Finance vs Performance", "Financial Power & On-Pitch Results",
               "Explore how financial strength relates to on-pitch outcomes across leagues, seasons, and clubs.")

# ── Filters ───────────────────────────────────────────────────────────────────
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

divider()

# ── Flourish scatter ──────────────────────────────────────────────────────────
st.markdown("#### Interactive Scatter — Squad Value vs Points")
flourish_embed(
    "PLACEHOLDER: https://flo.uri.sh/visualisation/YOUR_SCATTER_ID/embed",
    height=540,
    caption="Recommended: Flourish Scatter Plot — Squad Market Value (x) vs Points (y), coloured by League"
)

divider()

# ── Plotly scatter ────────────────────────────────────────────────────────────
st.markdown("#### Explore the Data")
col_x = st.selectbox("X-axis", ["svalue_m","spending_m"],
                     format_func=lambda x: "Squad Value (€M)" if x=="svalue_m" else "Transfer Spending (€M)")
col_y = st.selectbox("Y-axis", ["points","wins","goal_difference","position"],
                     format_func=lambda x: {"points":"Points","wins":"Wins",
                                            "goal_difference":"Goal Difference","position":"League Position"}[x])

fig_sc = px.scatter(dff, x=col_x, y=col_y,
                    color="league",
                    color_discrete_map=LEAGUE_COLORS,
                    hover_data=["club_name","season","league"],
                    trendline="ols",
                    labels={col_x: "Squad Value (€M)" if col_x=="svalue_m" else "Transfer Spending (€M)",
                            col_y: col_y.replace("_"," ").title()},
                    title=f"{'Squad Value' if col_x=='svalue_m' else 'Transfer Spending'} vs {col_y.replace('_',' ').title()}")
apply_template(fig_sc)
fig_sc.update_traces(marker=dict(size=7, opacity=0.75))
st.plotly_chart(fig_sc, use_container_width=True)

divider()

# ── Correlation heatmap ───────────────────────────────────────────────────────
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

# ── Correlation by league ─────────────────────────────────────────────────────
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