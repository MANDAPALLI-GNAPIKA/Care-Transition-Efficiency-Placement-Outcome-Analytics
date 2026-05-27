"""
Care Transition Efficiency & Placement Outcome Analytics
HHS Unaccompanied Alien Children Program — Streamlit Dashboard
Unified Mentor Internship Project
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="UAC Care Pipeline Analytics",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

.main { background-color: #0a0e1a; }
.stApp { background-color: #0a0e1a; }

.block-container {
    padding: 2rem 2rem 2rem 2rem;
    max-width: 100%;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f1628;
    border-right: 1px solid #1e2a45;
}

/* KPI cards */
.kpi-card {
    background: linear-gradient(135deg, #111827 0%, #1a2540 100%);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.5rem;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, #3b82f6, #06b6d4);
    border-radius: 12px 0 0 12px;
}
.kpi-label {
    font-size: 0.72rem;
    color: #64748b;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-family: 'IBM Plex Mono', monospace;
    margin-bottom: 0.3rem;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    color: #e2e8f0;
    line-height: 1;
    font-family: 'IBM Plex Mono', monospace;
}
.kpi-sub {
    font-size: 0.75rem;
    color: #94a3b8;
    margin-top: 0.3rem;
}
.kpi-delta-up { color: #34d399; }
.kpi-delta-down { color: #f87171; }

/* Alert box */
.alert-box {
    background: #1a0a0a;
    border: 1px solid #7f1d1d;
    border-left: 4px solid #ef4444;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.85rem;
    color: #fca5a5;
    font-family: 'IBM Plex Mono', monospace;
}
.alert-ok {
    background: #0a1a0f;
    border: 1px solid #14532d;
    border-left: 4px solid #22c55e;
    color: #86efac;
}
.alert-warn {
    background: #1a1500;
    border: 1px solid #713f12;
    border-left: 4px solid #f59e0b;
    color: #fcd34d;
}

/* Section headers */
.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #94a3b8;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-family: 'IBM Plex Mono', monospace;
    border-bottom: 1px solid #1e2a45;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}

/* Header banner */
.hero-banner {
    background: linear-gradient(135deg, #0f1628 0%, #1a2540 50%, #0f2240 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::after {
    content: '';
    position: absolute;
    top: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(59,130,246,0.06) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-size: 1.9rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.02em;
}
.hero-sub {
    color: #64748b;
    font-size: 0.9rem;
    font-family: 'IBM Plex Mono', monospace;
    margin: 0;
}
.hero-badge {
    display: inline-block;
    background: #1e3a5f;
    border: 1px solid #3b82f6;
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    font-size: 0.72rem;
    color: #93c5fd;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.1em;
    margin-bottom: 0.8rem;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background-color: #0f1628;
    border-radius: 10px;
    gap: 4px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #64748b;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.05em;
}
.stTabs [aria-selected="true"] {
    background-color: #1e3a5f !important;
    color: #93c5fd !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# DATA LOADING & PROCESSING
# ─────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("HHS_Unaccompanied_Alien_Children_Program.csv")
    df = df.dropna(subset=["Date"])
    df.columns = ["Date", "Apprehensions", "CBP_Custody", "Transfers", "HHS_Care_str", "Discharges"]
    df["Date"] = pd.to_datetime(df["Date"])
    df["HHS_Care"] = pd.to_numeric(df["HHS_Care_str"].str.replace(",", ""), errors="coerce")
    df = df.sort_values("Date").reset_index(drop=True)

    # Derived columns
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)
    df["DayOfWeek"] = df["Date"].dt.day_name()
    df["IsWeekend"] = df["Date"].dt.dayofweek >= 5

    # KPIs
    df["Transfer_Efficiency"] = (df["Transfers"] / df["CBP_Custody"]).replace([np.inf, -np.inf], np.nan)
    df["Discharge_Effectiveness"] = (df["Discharges"] / df["HHS_Care"]).replace([np.inf, -np.inf], np.nan)
    df["Pipeline_Throughput"] = ((df["Transfers"] + df["Discharges"]) / (df["Apprehensions"] + df["Transfers"])).replace([np.inf, -np.inf], np.nan)
    df["Backlog_Rate"] = df["Apprehensions"] - df["Discharges"]

    # Rolling metrics
    df["Discharge_Eff_30d"] = df["Discharge_Effectiveness"].rolling(30, min_periods=5).mean()
    df["Transfer_Eff_30d"] = df["Transfer_Efficiency"].rolling(30, min_periods=5).mean()
    df["Discharge_30d"] = df["Discharges"].rolling(30, min_periods=5).mean()
    df["Apprehensions_30d"] = df["Apprehensions"].rolling(30, min_periods=5).mean()

    return df


# Chart theme
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="IBM Plex Mono", color="#94a3b8", size=11),
    xaxis=dict(gridcolor="#1e2a45", linecolor="#1e2a45", tickfont=dict(size=10)),
    yaxis=dict(gridcolor="#1e2a45", linecolor="#1e2a45", tickfont=dict(size=10)),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
    margin=dict(t=30, b=40, l=10, r=10),
)
COLORS = {
    "blue": "#3b82f6",
    "cyan": "#06b6d4",
    "green": "#22c55e",
    "amber": "#f59e0b",
    "red": "#ef4444",
    "purple": "#a855f7",
    "slate": "#64748b",
}

# ─────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────
try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ Dataset not found. Place `HHS_Unaccompanied_Alien_Children_Program.csv` in the same folder as this script.")
    st.stop()

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="hero-badge">CONTROLS</div>', unsafe_allow_html=True)
    st.markdown("### Date Range")
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    date_range = st.date_input(
        "Select period",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    st.markdown("---")
    st.markdown("### Metric Toggles")
    show_transfer_eff = st.toggle("Transfer Efficiency Ratio", value=True)
    show_discharge_eff = st.toggle("Discharge Effectiveness Index", value=True)
    show_throughput = st.toggle("Pipeline Throughput Rate", value=True)
    show_backlog = st.toggle("Backlog Accumulation Rate", value=True)

    st.markdown("---")
    st.markdown("### Alert Thresholds")
    transfer_eff_threshold = st.slider("Transfer Efficiency Alert (min)", 0.0, 1.5, 0.4, 0.05)
    discharge_eff_threshold = st.slider("Discharge Effectiveness Alert (min)", 0.0, 0.1, 0.015, 0.001, format="%.3f")

    st.markdown("---")
    st.markdown("### View Mode")
    smoothing = st.toggle("Apply 30-day smoothing", value=True)

    st.markdown("---")
    st.caption("📊 HHS UAC Program Data\nJan 2023 – Dec 2025\n720 observations")

# Filter data
mask = (df["Date"].dt.date >= start_date) & (df["Date"].dt.date <= end_date)
dff = df[mask].copy()

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-badge">HHS / ORR</div>
    <h1 class="hero-title">Care Transition Efficiency & Placement Outcome Analytics</h1>
    <p class="hero-sub">UAC Pipeline: CBP Custody → HHS Care → Sponsor Placement</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# ALERT PANEL
# ─────────────────────────────────────────
recent = dff.tail(30)
recent_te = recent["Transfer_Efficiency"].mean()
recent_de = recent["Discharge_Effectiveness"].mean()

col_a1, col_a2, col_a3 = st.columns(3)

with col_a1:
    te_status = "alert-ok" if recent_te >= transfer_eff_threshold else "alert-box"
    te_icon = "✅" if recent_te >= transfer_eff_threshold else "⚠️"
    st.markdown(f'<div class="{te_status}">{te_icon} Transfer Efficiency (30d avg): <b>{recent_te:.3f}</b> — Threshold: {transfer_eff_threshold:.2f}</div>', unsafe_allow_html=True)

with col_a2:
    de_status = "alert-ok" if recent_de >= discharge_eff_threshold else "alert-box"
    de_icon = "✅" if recent_de >= discharge_eff_threshold else "⚠️"
    st.markdown(f'<div class="{de_status}">{de_icon} Discharge Effectiveness (30d avg): <b>{recent_de:.4f}</b> — Threshold: {discharge_eff_threshold:.3f}</div>', unsafe_allow_html=True)

with col_a3:
    stagnation_days = len(dff[(dff["Transfers"] < 20) & (dff["Discharges"] < 20)])
    stag_pct = stagnation_days / max(len(dff), 1) * 100
    stag_class = "alert-ok" if stag_pct < 20 else "alert-warn" if stag_pct < 50 else "alert-box"
    st.markdown(f'<div class="{stag_class}">🔍 Stagnation Days: <b>{stagnation_days}</b> ({stag_pct:.1f}% of period)</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────
st.markdown('<div class="section-title">Key Performance Indicators</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    val = dff["Apprehensions"].sum()
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Total Apprehensions</div>
        <div class="kpi-value">{val:,.0f}</div>
        <div class="kpi-sub">Daily avg: {dff['Apprehensions'].mean():.1f}</div>
    </div>""", unsafe_allow_html=True)

with k2:
    val = dff["Transfers"].sum()
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Total Transfers</div>
        <div class="kpi-value">{val:,.0f}</div>
        <div class="kpi-sub">CBP → HHS pipeline</div>
    </div>""", unsafe_allow_html=True)

with k3:
    val = dff["Discharges"].sum()
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Total Discharges</div>
        <div class="kpi-value">{val:,.0f}</div>
        <div class="kpi-sub">Sponsor placements</div>
    </div>""", unsafe_allow_html=True)

with k4:
    val = dff["Transfer_Efficiency"].mean()
    color = "kpi-delta-up" if val >= 0.5 else "kpi-delta-down"
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Transfer Efficiency</div>
        <div class="kpi-value">{val:.3f}</div>
        <div class="kpi-sub"><span class="{color}">Avg ratio (target ≥0.60)</span></div>
    </div>""", unsafe_allow_html=True)

with k5:
    val = dff["Discharge_Effectiveness"].mean()
    color = "kpi-delta-up" if val >= 0.025 else "kpi-delta-down"
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">Discharge Effectiveness</div>
        <div class="kpi-value">{val:.4f}</div>
        <div class="kpi-sub"><span class="{color}">Avg ratio (target ≥0.025)</span></div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# TABS
# ─────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Pipeline Flow",
    "⚡ Efficiency Metrics",
    "🔴 Bottleneck Detection",
    "📈 Outcome Trends",
    "📋 Executive Summary"
])

# ══════════════════════════════════════════
# TAB 1: PIPELINE FLOW
# ══════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">Care Pipeline Flow Visualization</div>', unsafe_allow_html=True)

    # Monthly aggregation
    monthly = dff.groupby("YearMonth").agg(
        Apprehensions=("Apprehensions", "sum"),
        Transfers=("Transfers", "sum"),
        Discharges=("Discharges", "sum"),
        CBP_Custody=("CBP_Custody", "mean"),
        HHS_Care=("HHS_Care", "mean"),
    ).reset_index()

    # Stacked flow chart
    fig_flow = go.Figure()
    fig_flow.add_trace(go.Bar(
        x=monthly["YearMonth"], y=monthly["Apprehensions"],
        name="Apprehensions", marker_color=COLORS["red"], opacity=0.85,
    ))
    fig_flow.add_trace(go.Bar(
        x=monthly["YearMonth"], y=monthly["Transfers"],
        name="Transfers (CBP→HHS)", marker_color=COLORS["blue"], opacity=0.85,
    ))
    fig_flow.add_trace(go.Bar(
        x=monthly["YearMonth"], y=monthly["Discharges"],
        name="Discharges (HHS→Sponsor)", marker_color=COLORS["green"], opacity=0.85,
    ))
    fig_flow.update_layout(
        barmode="group",
        title="Monthly Flow: Apprehensions vs Transfers vs Discharges",
        height=380,
        **PLOTLY_THEME
    )
    st.plotly_chart(fig_flow, use_container_width=True)

    col_l, col_r = st.columns(2)

    with col_l:
        # CBP vs HHS Stock over time
        fig_stock = go.Figure()
        fig_stock.add_trace(go.Scatter(
            x=dff["Date"], y=dff["CBP_Custody"],
            name="CBP Custody", line=dict(color=COLORS["amber"], width=1.5),
            fill="tozeroy", fillcolor="rgba(245,158,11,0.07)"
        ))
        fig_stock.add_trace(go.Scatter(
            x=dff["Date"], y=dff["HHS_Care"],
            name="HHS Care", line=dict(color=COLORS["blue"], width=2),
            fill="tozeroy", fillcolor="rgba(59,130,246,0.07)"
        ))
        fig_stock.update_layout(
            title="Stock Levels: CBP Custody vs HHS Care",
            height=300, **PLOTLY_THEME
        )
        st.plotly_chart(fig_stock, use_container_width=True)

    with col_r:
        # Sankey / pipeline balance
        fig_bal = go.Figure()
        fig_bal.add_trace(go.Scatter(
            x=dff["Date"],
            y=(dff["Discharges"] - dff["Apprehensions"]).rolling(30, min_periods=5).mean(),
            name="Net Flow (Discharges − Apprehensions)",
            line=dict(color=COLORS["cyan"], width=2),
            fill="tozeroy",
            fillcolor="rgba(6,182,212,0.08)"
        ))
        fig_bal.add_hline(y=0, line_dash="dash", line_color=COLORS["slate"], line_width=1)
        fig_bal.update_layout(
            title="Net Flow Balance (30d avg) — Positive = System Clearing",
            height=300, **PLOTLY_THEME
        )
        st.plotly_chart(fig_bal, use_container_width=True)

# ══════════════════════════════════════════
# TAB 2: EFFICIENCY METRICS
# ══════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">Transfer & Discharge Efficiency Panels</div>', unsafe_allow_html=True)

    col_e1, col_e2 = st.columns(2)

    with col_e1:
        if show_transfer_eff:
            y_col = "Transfer_Eff_30d" if smoothing else "Transfer_Efficiency"
            fig_te = go.Figure()
            fig_te.add_trace(go.Scatter(
                x=dff["Date"], y=dff[y_col],
                name="Transfer Efficiency",
                line=dict(color=COLORS["blue"], width=2),
                fill="tozeroy", fillcolor="rgba(59,130,246,0.08)"
            ))
            fig_te.add_hline(y=0.6, line_dash="dot", line_color=COLORS["green"],
                             annotation_text="Target ≥0.60", annotation_font_color=COLORS["green"])
            fig_te.add_hline(y=transfer_eff_threshold, line_dash="dash", line_color=COLORS["red"],
                             annotation_text=f"Alert Threshold", annotation_font_color=COLORS["red"])
            fig_te.update_layout(
                title="Transfer Efficiency Ratio (Transfers ÷ CBP Custody)",
                height=320, **PLOTLY_THEME
            )
            st.plotly_chart(fig_te, use_container_width=True)
        else:
            st.info("Transfer Efficiency Ratio is toggled off in the sidebar.")

    with col_e2:
        if show_discharge_eff:
            y_col2 = "Discharge_Eff_30d" if smoothing else "Discharge_Effectiveness"
            fig_de = go.Figure()
            fig_de.add_trace(go.Scatter(
                x=dff["Date"], y=dff[y_col2],
                name="Discharge Effectiveness",
                line=dict(color=COLORS["green"], width=2),
                fill="tozeroy", fillcolor="rgba(34,197,94,0.08)"
            ))
            fig_de.add_hline(y=0.025, line_dash="dot", line_color=COLORS["cyan"],
                             annotation_text="Target ≥0.025", annotation_font_color=COLORS["cyan"])
            fig_de.add_hline(y=discharge_eff_threshold, line_dash="dash", line_color=COLORS["red"],
                             annotation_text="Alert Threshold", annotation_font_color=COLORS["red"])
            fig_de.update_layout(
                title="Discharge Effectiveness Index (Discharges ÷ HHS Care)",
                height=320, **PLOTLY_THEME
            )
            st.plotly_chart(fig_de, use_container_width=True)
        else:
            st.info("Discharge Effectiveness Index is toggled off in the sidebar.")

    col_e3, col_e4 = st.columns(2)

    with col_e3:
        if show_throughput:
            y_pt = dff["Pipeline_Throughput"].rolling(30, min_periods=5).mean() if smoothing else dff["Pipeline_Throughput"]
            fig_pt = go.Figure()
            fig_pt.add_trace(go.Scatter(
                x=dff["Date"], y=y_pt,
                name="Pipeline Throughput",
                line=dict(color=COLORS["purple"], width=2),
                fill="tozeroy", fillcolor="rgba(168,85,247,0.07)"
            ))
            fig_pt.add_hline(y=1.0, line_dash="dot", line_color=COLORS["slate"],
                             annotation_text="Equilibrium", annotation_font_color=COLORS["slate"])
            fig_pt.update_layout(
                title="Pipeline Throughput Rate ((Transfers+Discharges)÷(Apprehensions+Transfers))",
                height=300, **PLOTLY_THEME
            )
            st.plotly_chart(fig_pt, use_container_width=True)

    with col_e4:
        if show_backlog:
            y_br = dff["Backlog_Rate"].rolling(30, min_periods=5).mean() if smoothing else dff["Backlog_Rate"]
            fig_br = go.Figure()
            fig_br.add_trace(go.Scatter(
                x=dff["Date"], y=y_br,
                name="Backlog Rate",
                line=dict(color=COLORS["amber"], width=2),
                fill="tozeroy", fillcolor="rgba(245,158,11,0.07)"
            ))
            fig_br.add_hline(y=0, line_dash="dash", line_color=COLORS["slate"],
                             annotation_text="Break-even", annotation_font_color=COLORS["slate"])
            fig_br.update_layout(
                title="Backlog Accumulation Rate (Apprehensions − Discharges)",
                height=300, **PLOTLY_THEME
            )
            st.plotly_chart(fig_br, use_container_width=True)

    # Day-of-week heatmap
    st.markdown("---")
    st.markdown('<div class="section-title">Day-of-Week Pattern Analysis</div>', unsafe_allow_html=True)

    dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dow = dff.groupby("DayOfWeek")[["Apprehensions", "Transfers", "Discharges", "Transfer_Efficiency", "Discharge_Effectiveness"]].mean().round(3)
    dow = dow.reindex([d for d in dow_order if d in dow.index])

    fig_dow = px.bar(
        dow.reset_index(), x="DayOfWeek", y=["Apprehensions", "Transfers", "Discharges"],
        barmode="group",
        color_discrete_map={"Apprehensions": COLORS["red"], "Transfers": COLORS["blue"], "Discharges": COLORS["green"]},
        title="Average Daily Flow by Day of Week"
    )
    fig_dow.update_layout(height=300, **PLOTLY_THEME)
    st.plotly_chart(fig_dow, use_container_width=True)

# ══════════════════════════════════════════
# TAB 3: BOTTLENECK DETECTION
# ══════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">Bottleneck Detection & Delay Analysis</div>', unsafe_allow_html=True)

    # Identify bottleneck days
    q75_hhs = dff["HHS_Care"].quantile(0.75)
    q25_dis = dff["Discharges"].quantile(0.25)
    bottleneck_mask = (dff["HHS_Care"] > q75_hhs) & (dff["Discharges"] < q25_dis)
    stagnation_mask = (dff["Transfers"] < 20) & (dff["Discharges"] < 20)

    col_b1, col_b2 = st.columns([3, 1])

    with col_b1:
        fig_bn = go.Figure()
        # HHS Care area
        fig_bn.add_trace(go.Scatter(
            x=dff["Date"], y=dff["HHS_Care"],
            name="HHS Care (stock)", line=dict(color=COLORS["blue"], width=2),
            fill="tozeroy", fillcolor="rgba(59,130,246,0.06)"
        ))
        # Bottleneck highlights
        bn_days = dff[bottleneck_mask]
        fig_bn.add_trace(go.Scatter(
            x=bn_days["Date"], y=bn_days["HHS_Care"],
            mode="markers", name="Bottleneck Day",
            marker=dict(color=COLORS["red"], size=5, symbol="x")
        ))
        # Stagnation highlights
        st_days = dff[stagnation_mask]
        fig_bn.add_trace(go.Scatter(
            x=st_days["Date"], y=st_days["HHS_Care"],
            mode="markers", name="Stagnation Day",
            marker=dict(color=COLORS["amber"], size=4, symbol="circle-open")
        ))
        fig_bn.add_hline(y=q75_hhs, line_dash="dot", line_color=COLORS["red"],
                         annotation_text=f"75th pct ({q75_hhs:,.0f})", annotation_font_color=COLORS["red"])
        fig_bn.update_layout(
            title="HHS Care Census with Bottleneck & Stagnation Markers",
            height=380, **PLOTLY_THEME
        )
        st.plotly_chart(fig_bn, use_container_width=True)

    with col_b2:
        st.markdown("**Bottleneck Summary**")
        st.metric("Bottleneck Days", int(bottleneck_mask.sum()))
        st.metric("Stagnation Days", int(stagnation_mask.sum()))
        st.metric("Peak HHS Census", f"{dff['HHS_Care'].max():,.0f}")
        st.metric("75th Pct HHS", f"{q75_hhs:,.0f}")
        st.markdown("---")
        st.markdown("""
**Bottleneck = HHS Care > 75th pct AND Discharges < 25th pct**

**Stagnation = Transfers < 20 AND Discharges < 20**
        """)

    # Monthly bottleneck frequency
    dff_copy = dff.copy()
    dff_copy["Bottleneck"] = bottleneck_mask.values
    dff_copy["Stagnation"] = stagnation_mask.values
    monthly_bn = dff_copy.groupby("YearMonth").agg(
        Bottleneck_Days=("Bottleneck", "sum"),
        Stagnation_Days=("Stagnation", "sum"),
        Avg_HHS=("HHS_Care", "mean"),
    ).reset_index()

    fig_bn2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig_bn2.add_trace(go.Bar(
        x=monthly_bn["YearMonth"], y=monthly_bn["Bottleneck_Days"],
        name="Bottleneck Days", marker_color=COLORS["red"], opacity=0.7
    ), secondary_y=False)
    fig_bn2.add_trace(go.Scatter(
        x=monthly_bn["YearMonth"], y=monthly_bn["Avg_HHS"],
        name="Avg HHS Care", line=dict(color=COLORS["blue"], width=2)
    ), secondary_y=True)
    fig_bn2.update_layout(title="Monthly Bottleneck Frequency vs HHS Care Level", height=300, **PLOTLY_THEME)
    fig_bn2.update_yaxes(title_text="Bottleneck Days", secondary_y=False, gridcolor="#1e2a45")
    fig_bn2.update_yaxes(title_text="Avg HHS Care", secondary_y=True, gridcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_bn2, use_container_width=True)

    # Year breakdown
    st.markdown('<div class="section-title">Year-over-Year Bottleneck Comparison</div>', unsafe_allow_html=True)
    yearly_bn = dff_copy.groupby("Year").agg(
        Total_Days=("Date", "count"),
        Bottleneck_Days=("Bottleneck", "sum"),
        Stagnation_Days=("Stagnation", "sum"),
        Avg_HHS=("HHS_Care", "mean"),
        Avg_Transfer_Eff=("Transfer_Efficiency", "mean"),
        Avg_Discharge_Eff=("Discharge_Effectiveness", "mean"),
    ).reset_index()
    yearly_bn["Bottleneck_Pct"] = (yearly_bn["Bottleneck_Days"] / yearly_bn["Total_Days"] * 100).round(1)
    yearly_bn["Stagnation_Pct"] = (yearly_bn["Stagnation_Days"] / yearly_bn["Total_Days"] * 100).round(1)
    st.dataframe(
        yearly_bn[["Year", "Total_Days", "Bottleneck_Days", "Bottleneck_Pct",
                   "Stagnation_Days", "Stagnation_Pct", "Avg_HHS",
                   "Avg_Transfer_Eff", "Avg_Discharge_Eff"]].round(4),
        use_container_width=True, hide_index=True
    )

# ══════════════════════════════════════════
# TAB 4: OUTCOME TRENDS
# ══════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">Placement Outcome Trend Analysis</div>', unsafe_allow_html=True)

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        # Discharge trend
        monthly = dff.groupby("YearMonth").agg(
            Discharges=("Discharges", "sum"),
            Apprehensions=("Apprehensions", "sum"),
            Discharge_Eff=("Discharge_Effectiveness", "mean"),
        ).reset_index()
        fig_dtrend = go.Figure()
        fig_dtrend.add_trace(go.Scatter(
            x=monthly["YearMonth"], y=monthly["Discharges"],
            name="Monthly Discharges",
            line=dict(color=COLORS["green"], width=2),
            fill="tozeroy", fillcolor="rgba(34,197,94,0.07)"
        ))
        fig_dtrend.add_trace(go.Scatter(
            x=monthly["YearMonth"], y=monthly["Apprehensions"],
            name="Monthly Apprehensions",
            line=dict(color=COLORS["red"], width=2, dash="dot"),
        ))
        fig_dtrend.update_layout(
            title="Monthly Discharges vs Apprehensions",
            height=320, **PLOTLY_THEME
        )
        st.plotly_chart(fig_dtrend, use_container_width=True)

    with col_t2:
        # Outcome stability (rolling std)
        dff_sorted = dff.sort_values("Date")
        rolling_std = dff_sorted["Discharge_Effectiveness"].rolling(30, min_periods=10).std()
        fig_stab = go.Figure()
        fig_stab.add_trace(go.Scatter(
            x=dff_sorted["Date"], y=rolling_std,
            name="30d Std Dev of Discharge Effectiveness",
            line=dict(color=COLORS["amber"], width=2),
            fill="tozeroy", fillcolor="rgba(245,158,11,0.07)"
        ))
        fig_stab.update_layout(
            title="Outcome Stability Score (lower = more consistent)",
            height=320, **PLOTLY_THEME
        )
        st.plotly_chart(fig_stab, use_container_width=True)

    # Year over year comparison
    yearly = dff.groupby("Year").agg(
        Apprehensions=("Apprehensions", "sum"),
        Transfers=("Transfers", "sum"),
        Discharges=("Discharges", "sum"),
        Avg_HHS=("HHS_Care", "mean"),
        Avg_Transfer_Eff=("Transfer_Efficiency", "mean"),
        Avg_Discharge_Eff=("Discharge_Effectiveness", "mean"),
    ).reset_index()

    fig_yoy = go.Figure()
    metrics = ["Apprehensions", "Transfers", "Discharges"]
    colors = [COLORS["red"], COLORS["blue"], COLORS["green"]]
    for m, c in zip(metrics, colors):
        fig_yoy.add_trace(go.Bar(
            x=yearly["Year"].astype(str), y=yearly[m],
            name=m, marker_color=c, opacity=0.85
        ))
    fig_yoy.update_layout(
        barmode="group",
        title="Year-over-Year Totals: Apprehensions, Transfers, Discharges",
        height=320, **PLOTLY_THEME
    )
    st.plotly_chart(fig_yoy, use_container_width=True)

    # Monthly discharge effectiveness scatter
    monthly2 = dff.groupby("YearMonth").agg(
        Discharge_Eff=("Discharge_Effectiveness", "mean"),
        HHS_Care=("HHS_Care", "mean"),
        Discharges=("Discharges", "sum"),
    ).reset_index()
    monthly2["Year"] = monthly2["YearMonth"].str[:4]

    fig_scatter = px.scatter(
        monthly2,
        x="HHS_Care", y="Discharge_Eff",
        color="Year",
        size="Discharges",
        hover_data=["YearMonth"],
        title="Discharge Effectiveness vs HHS Care Load (Monthly)",
        color_discrete_map={"2023": COLORS["amber"], "2024": COLORS["blue"], "2025": COLORS["green"]},
    )
    fig_scatter.update_layout(height=340, **PLOTLY_THEME)
    st.plotly_chart(fig_scatter, use_container_width=True)

# ══════════════════════════════════════════
# TAB 5: EXECUTIVE SUMMARY
# ══════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">Executive Summary for Government Stakeholders</div>', unsafe_allow_html=True)

    # Filtered period summary
    total_days = len(dff)
    period_label = f"{start_date.strftime('%b %d, %Y')} – {end_date.strftime('%b %d, %Y')}"

    st.markdown(f"**Analysis Period:** {period_label} ({total_days} reporting days)")
    st.markdown("---")

    # 3-column summary grid
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("**📥 Intake Pipeline**")
        st.metric("Total Apprehensions", f"{dff['Apprehensions'].sum():,.0f}")
        st.metric("Total Transfers to HHS", f"{dff['Transfers'].sum():,.0f}")
        st.metric("Peak CBP Custody", f"{dff['CBP_Custody'].max():,.0f}")
        st.metric("Avg Daily Apprehensions", f"{dff['Apprehensions'].mean():.1f}")

    with c2:
        st.markdown("**🏠 HHS Care Operations**")
        st.metric("Peak HHS Census", f"{dff['HHS_Care'].max():,.0f}")
        st.metric("Min HHS Census", f"{dff['HHS_Care'].min():,.0f}")
        st.metric("Avg HHS Census", f"{dff['HHS_Care'].mean():,.0f}")
        st.metric("Total Discharges", f"{dff['Discharges'].sum():,.0f}")

    with c3:
        st.markdown("**📊 Process Efficiency**")
        st.metric("Avg Transfer Efficiency", f"{dff['Transfer_Efficiency'].mean():.3f}")
        st.metric("Avg Discharge Effectiveness", f"{dff['Discharge_Effectiveness'].mean():.4f}")
        st.metric("Stagnation Days", f"{int(stagnation_mask.sum())}")
        net_flow = dff['Discharges'].sum() - dff['Apprehensions'].sum()
        st.metric("Net Flow (Discharges−Apprehensions)", f"{net_flow:+,.0f}")

    st.markdown("---")
    st.markdown("### Key Findings")

    findings = [
        ("🔵 Transfer Stage Is Efficient", f"Average Transfer Efficiency of {dff['Transfer_Efficiency'].mean():.3f} indicates children move quickly from CBP to HHS custody. This stage is not the primary bottleneck."),
        ("🔴 HHS→Sponsor Discharge Is the Bottleneck Stage", f"Discharge Effectiveness averaged {dff['Discharge_Effectiveness'].mean():.4f} — meaning less than 3% of the HHS care stock is placed daily. This is where delays compound."),
        ("📉 2025 Reflects Policy-Driven Contraction", "The dramatic reduction in all metrics in 2025 is consistent with enforcement changes under the incoming administration, not an organic efficiency improvement."),
        ("⚠️ Peak Stress Was December 2023", f"HHS Care peaked at {dff['HHS_Care'].max():,} children. The system successfully drew down this census over the following year, demonstrating surge response capacity."),
        ("📊 Discharges Outpaced Apprehensions System-Wide", f"Over the analysis period, net flow was +{net_flow:,.0f} (more discharges than apprehensions), meaning the system was a net reducer of backlog."),
    ]

    for title, body in findings:
        with st.expander(title):
            st.write(body)

    st.markdown("### Recommendations")
    st.markdown("""
1. **Monitor Discharge Effectiveness as primary KPI**, not just headcount — it reveals whether the HHS→Sponsor stage is functioning
2. **Set threshold alerts** at Transfer Efficiency < 0.40 and Discharge Effectiveness < 0.015 for early bottleneck warning
3. **Publish pipeline metrics publicly** alongside the existing daily census to enable accountability
4. **Investigate the 2025 contraction** to distinguish reduced harm (fewer border crossings) from reduced access (processing slowdowns)
5. **Weekend discharge patterns** require further study — higher discharge rates on Fridays/weekends may be reporting artifacts
    """)

    st.markdown("---")
    st.caption("Dashboard  | HHS UAC Program Analytics | Data: Jan 2023 – Dec 2025")
Unif
