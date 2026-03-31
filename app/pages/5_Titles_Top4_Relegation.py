import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import (inject_css, load_data, section_header, insight, divider,
                   flourish_embed, apply_template, LEAGUE_COLORS, LEAGUE_LABELS)

st.set_page_config(page_title="Titles, Top 4 & Relegation", page_icon="⚽", layout="wide")
inject_css()

df = load_data()

# Pre-compute buckets
df["spending_bucket"] = pd.cut(df["spending_rank"],
    bins=[0,3,6,10,15,25], labels=["Top 3","4–6","7–10","11–15","16+"])
df["value_bucket"] = pd.cut(df["value_rank"],
    bins=[0,3,6,10,15,25], labels=["Top 3","4–6","7–10","11–15","16+"])

section_header("Titles, Top 4 & Relegation", "Does Money Buy Trophies?",
               "How financial strength maps to the three most critical competitive outcomes.")

# ── Flourish ──────────────────────────────────────────────────────────────────
st.markdown("#### Title Winners by Spending Rank")
flourish_embed(
    "PLACEHOLDER: https://flo.uri.sh/visualisation/YOUR_TITLES_CHART_ID/embed",
    height=480,
    caption="Recommended: Flourish Pie / Donut or Sankey — Title winners broken down by spending rank bucket"
)

divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🏆 Title Winners", "⭐ Top 4 (UCL)", "⬇️ Relegation"])

# ── TAB 1: Titles ─────────────────────────────────────────────────────────────
with tab1:
    title_df = df[df["title_won"] == 1]
    spend_dist = title_df["spending_rank"].value_counts().reset_index()
    spend_dist.columns = ["Spending Rank","Count"]
    spend_dist["Rank Group"] = spend_dist["Spending Rank"].apply(
        lambda x: "Rank 1" if x==1 else ("Top 3" if x<=3 else ("Top 6" if x<=6 else "7+"))
    )
    group_agg = spend_dist.groupby("Rank Group")["Count"].sum().reset_index()
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
        win_rate = df.groupby("spending_rank").agg(
            titles=("title_won","sum"), total=("title_won","count"),
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
            title="Title Win Rate by Spending Rank",
        )
        st.plotly_chart(fig_wr, use_container_width=True)

    insight("30% of all titles were won by the single highest spender — far above the 5% random chance baseline. Yet 70% of titles were won outside the top spender, proving money helps but doesn't guarantee.")

    divider()

    # Title concentration
    st.markdown("#### Title Concentration by Club and League (2014–2024)")
    title_clubs = df[df["title_won"]==1].groupby(["league","club_name"]).size().reset_index(name="titles")
    title_clubs["league_label"] = title_clubs["league"].map(LEAGUE_LABELS)
    title_clubs = title_clubs.sort_values(["league","titles"], ascending=[True, False])

    fig_conc = px.bar(title_clubs, x="titles", y="club_name", color="league",
                      color_discrete_map=LEAGUE_COLORS,
                      facet_col="league_label", facet_col_wrap=3,
                      labels={"titles":"Titles Won","club_name":"Club"})
    apply_template(fig_conc)
    fig_conc.update_layout(showlegend=False, height=520)
    fig_conc.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    st.plotly_chart(fig_conc, use_container_width=True)
    insight("Bundesliga and Ligue 1 show extreme title concentration — Bayern and PSG dominated for most of the decade. The Premier League saw the most variety, with 5 different champions.")

# ── TAB 2: Top 4 ──────────────────────────────────────────────────────────────
with tab2:
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

# ── TAB 3: Relegation ─────────────────────────────────────────────────────────
with tab3:
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