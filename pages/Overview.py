import streamlit as st
import plotly.express as px
import pandas as pd

from utils.load_data import load_data
from utils.filters import sidebar_filters

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Overview",
    page_icon="🍽️",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
/* Remove heavy top padding */
.block-container {
    padding-top: 1.5rem;
}

/* Hero Section */
.hero-container {
    background: linear-gradient(135deg, #0F172A, #1E293B);
    padding: 2.5rem;
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.5px;
}

.hero-subtitle {
    font-size: 16px;
    color: #94A3B8;
    margin-top: 10px;
}

/* KPI Cards */
.metric-card {
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 25px 20px;
    border-radius: 16px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 20px rgba(0, 230, 118, 0.15);
    border: 1px solid #00E676;
}

.metric-title {
    color: #64748B;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
    font-weight: 600;
}

.metric-value {
    color: #FFFFFF;
    font-size: 32px;
    font-weight: 800;
}

/* Insight Box */
.insight-box {
    padding: 25px;
    border-radius: 16px;
    background: rgba(30, 41, 59, 0.3);
    border-left: 5px solid #00E676;
    border-top: 1px solid rgba(255, 255, 255, 0.03);
    border-right: 1px solid rgba(255, 255, 255, 0.03);
    border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    margin-top: 25px;
}

.insight-title {
    font-size: 20px;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 15px;
}

.insight-item {
    font-size: 15px;
    color: #94A3B8;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class='hero-container'>
    <div class='hero-title'>🍽️ Restaurant Intelligence Dashboard</div>
    <div class='hero-subtitle'>
        Executive operations suite for monitoring real-time revenue cycles, volume velocity, and product contributions.
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# DATA PROCESSING
# ============================================================
df = load_data()
df = sidebar_filters(df)

# Safeguard parsing of date formats safely
if not df.empty and "Order_Date" in df.columns:
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# ============================================================
# KPI CALCULATIONS
# ============================================================
total_revenue = df["Total_Amount"].sum() if not df.empty else 0
total_orders = len(df)
total_customers = df["Customer_ID"].nunique() if not df.empty else 0

if not df.empty and "Rating" in df.columns:
    ratings = pd.to_numeric(df["Rating"], errors="coerce")
    avg_rating = round(ratings.mean(), 1) if ratings.notna().sum() > 0 else 0.0
else:
    avg_rating = 0.0

# ============================================================
# KPI CARDS DISPLAY
# ============================================================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Gross Revenue</div><div class='metric-value'>₹{total_revenue:,.0f}</div></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Orders Processed</div><div class='metric-value'>{total_orders:,}</div></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Unique Customers</div><div class='metric-value'>{total_customers:,}</div></div>", unsafe_allow_html=True)
with c4:
    st.markdown(f"<div class='metric-card'><div class='metric-title'>Average Rating</div><div class='metric-value'>⭐ {avg_rating}</div></div>", unsafe_allow_html=True)

st.write("")

# ============================================================
# GLOBAL PLOTLY THEME
# ============================================================
def apply_dope_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", size=13, color="#E2E8F0"),
        hovermode="x unified" if fig.layout.hovermode is None else fig.layout.hovermode,
        margin=dict(l=10, r=10, t=50, b=10),
        legend=dict(orientation="h", y=1.12, x=0.01),
        title_x=0.01,
        title_font=dict(size=18, family="Inter, sans-serif", color="#FFFFFF")
    )
    
    # Only apply axes treatments to charts containing cartesian structures
    if hasattr(fig, "update_xaxes"):
        fig.update_xaxes(showgrid=False, zeroline=False)
    if hasattr(fig, "update_yaxes"):
        fig.update_yaxes(gridcolor='rgba(255,255,255,0.05)', zeroline=False)
        
    return fig

# ============================================================
# REVENUE TREND
# ============================================================
if not df.empty:
    # Build clean string sorting chronologically from actual pandas Datetime objects
    df['Year_Month'] = df['Order_Date'].dt.to_period('M')
    monthly_sales = df.groupby('Year_Month')["Total_Amount"].sum().reset_index()
    monthly_sales['Month_Label'] = monthly_sales['Year_Month'].dt.strftime('%b %Y')
    monthly_sales = monthly_sales.sort_values('Year_Month')

    fig_area = px.area(
        monthly_sales,
        x="Month_Label",
        y="Total_Amount",
        title="📈 Monthly Revenue Trajectory",
        markers=True,
        color_discrete_sequence=["#00E676"]
    )
    fig_area.update_traces(line=dict(width=3), fill='tozeroy', fillcolor='rgba(0, 230, 118, 0.08)')
    st.plotly_chart(apply_dope_theme(fig_area), use_container_width=True)

# ============================================================
# SECOND ROW
# ============================================================
col1, col2 = st.columns(2)

with col1:
    if not df.empty:
        category_sales = (
            df.groupby("Category")["Total_Amount"]
            .sum()
            .reset_index()
            .sort_values(by="Total_Amount", ascending=True)
        )
        fig_bar = px.bar(
            category_sales,
            x="Total_Amount",
            y="Category",
            orientation="h",
            color="Total_Amount",
            color_continuous_scale="Viridis",
            title="🍔 Revenue Distribution by Category"
        )
        fig_bar.update_layout(coloraxis_showscale=False)
        st.plotly_chart(apply_dope_theme(fig_bar), use_container_width=True)

with col2:
    if not df.empty:
        fig_sun = px.sunburst(
            df,
            path=["Order_Type", "Category"],
            values="Total_Amount",
            title="📦 Order Allocation Mechanics",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        # Avoid cartesian unified hover templates breaking sunburst structures
        fig_sun.update_layout(hovermode=False)
        st.plotly_chart(apply_dope_theme(fig_sun), use_container_width=True)

# ============================================================
# TREEMAP (ITEM CONTRIBUTION)
# ============================================================
st.write("") # Clean native spacing instead of raw HTML break
st.subheader("🔥 Item Contribution Breakdown")

if not df.empty:
    fig_tree = px.treemap(
        df,
        path=["Category", "Menu_Item"],
        values="Total_Amount",
        color="Total_Amount",
        color_continuous_scale="Viridis",
        title="Menu Item Revenue Hierarchy" # Title added inside the chart
    )
    
    # Hide standard hovermode for treemaps to prevent layout text clashing
    fig_tree.update_layout(hovermode=False)
    
    # Apply theme and render
    st.plotly_chart(apply_dope_theme(fig_tree), use_container_width=True)

# ============================================================
# BUSINESS INSIGHTS
# ============================================================
if not df.empty and 'category_sales' in locals() and not category_sales.empty:
    top_category = category_sales.sort_values(by="Total_Amount", ascending=False).iloc[0]["Category"]
else:
    top_category = "N/A"

st.markdown(f"""
<div class='insight-box'>
    <div class='insight-title'>📌 Operational Synthesis Summary</div>
    <div class='insight-item'>🚀 Leading Product Velocity Engine: <b>{top_category}</b></div>
    <div class='insight-item'>💰 Total Pipeline Capital Velocity: <b>₹{total_revenue:,.0f}</b></div>
    <div class='insight-item'>⭐ System-Wide Satisfaction Mean: <b>{avg_rating} / 5.0</b></div>
    <div class='insight-item'>🧾 Closed Settlement Transactions: <b>{total_orders:,} items</b></div>
</div>
""", unsafe_allow_html=True)