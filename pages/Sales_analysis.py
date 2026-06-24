# ============================================================
# IMPORT LIBRARIES
# ============================================================

import streamlit as st          # For creating dashboard UI
import plotly.express as px     # For interactive charts
import pandas as pd             # For data manipulation

# Import custom functions
from utils.load_data import load_data
from utils.filters import sidebar_filters


# ============================================================
# MODERN STYLING (CUSTOM CSS)
# ============================================================

st.set_page_config(
    page_title="Sales Analysis",
    page_icon="🍽️",
    layout="wide"
)

st.markdown("""
<style>

/* KPI Card Styling */

.sales-metric-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 20px;
    text-align: center;
    transition: 0.3s;
}

.sales-metric-card:hover {
    transform: translateY(-5px);
    border: 1px solid #00E676;
    box-shadow: 0px 10px 25px rgba(0,230,118,0.15);
}

.sales-metric-label {
    font-size: 13px;
    color: #A0A0A0;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}

.sales-metric-val {
    font-size: 28px;
    color: white;
    font-weight: 700;
}

/* Hero Section */

.hero {
    padding: 2rem;
    border-radius: 20px;
    background: linear-gradient(135deg,#111827,#1E293B);
    border:1px solid rgba(255,255,255,0.08);
}

.hero-title {
    font-size:42px;
    font-weight:800;
    color:white;
}

.hero-subtitle {
    color:#94A3B8;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HERO HEADER
# ============================================================

st.markdown("""
<div class='hero'>

<div class='hero-title'>
📈 Sales Intelligence Dashboard
</div>

<div class='hero-subtitle'>
Analyze revenue trends, peak sales periods,
payment behavior, and category performance.
</div>

</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

# Load dataset
df = load_data()

# Apply sidebar filters
df = sidebar_filters(df)

# Stop execution if no records found
if df.empty:
    st.warning("⚠️ No data available for selected filters.")
    st.stop()

# Convert date column to datetime format
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Create string version of date for charts
df["Order_Date_Str"] = (
    df["Order_Date"]
    .dt.strftime("%Y-%m-%d")
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

# Total revenue generated
total_revenue = df["Total_Amount"].sum()


# Daily sales summary

daily_sales = (
    df.groupby("Order_Date_Str")
    ["Total_Amount"]
    .sum()
)

# Find highest revenue day

peak_day_str = daily_sales.idxmax()

peak_day_val = daily_sales.max()

peak_day_formatted = (
    f"{pd.to_datetime(peak_day_str).strftime('%d %b %Y')}"
    f" (₹{peak_day_val:,.0f})"
)


# Average amount spent per order

avg_ticket = round(
    df["Total_Amount"].mean(),
    2
)


# Most used payment method

top_payment = (
    df["Payment_Method"]
    .mode()[0]
)


# ============================================================
# DISPLAY KPI CARDS
# ============================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class='sales-metric-card'>
        <div class='sales-metric-label'>
        💰 Total Revenue
        </div>
        <div class='sales-metric-val'>
        ₹{total_revenue:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class='sales-metric-card'>
        <div class='sales-metric-label'>
        🏆 Peak Revenue Day
        </div>
        <div class='sales-metric-val'>
        {peak_day_formatted}
        </div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class='sales-metric-card'>
        <div class='sales-metric-label'>
        💳 Avg Ticket Value
        </div>
        <div class='sales-metric-val'>
        ₹{avg_ticket:,.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class='sales-metric-card'>
        <div class='sales-metric-label'>
        ⚡ Preferred Payment
        </div>
        <div class='sales-metric-val'>
        {top_payment}
        </div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# GLOBAL PLOTLY THEME
# ============================================================

def apply_sales_theme(fig):

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',

        font=dict(
            family="Inter",
            size=13
        ),

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        hovermode="x unified",

        title_x=0.02
    )

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(
        gridcolor='rgba(255,255,255,0.06)'
    )

    return fig


# ============================================================
# MONTHLY REVENUE TREND
# ============================================================

# Group revenue month-wise

monthly_sales = (
    df.groupby(
        df["Order_Date"].dt.to_period("M")
    )["Total_Amount"]

    .sum()

    .reset_index()
)

monthly_sales["Month"] = (
    monthly_sales["Order_Date"]
    .astype(str)
)

# Create area chart

fig = px.area(

    monthly_sales,

    x="Month",
    y="Total_Amount",

    title="📈 Monthly Revenue Trend",

    markers=True
)

fig.update_traces(
    line=dict(width=4)
)

st.plotly_chart(
    apply_sales_theme(fig),
    use_container_width=True
)


# ============================================================
# TOP REVENUE DAYS
# ============================================================

top_days = (

    df.groupby("Order_Date_Str")
    ["Total_Amount"]

    .sum()

    .reset_index()

    .sort_values(
        by="Total_Amount",
        ascending=True
    )

    .tail(10)
)

fig = px.bar(

    top_days,

    x="Total_Amount",
    y="Order_Date_Str",

    orientation="h",

    title="🏆 Top 10 Revenue Generating Days",

    color="Total_Amount",

    color_continuous_scale="Cividis"
)

fig.update_layout(
    coloraxis_showscale=False
)

st.plotly_chart(
    apply_sales_theme(fig),
    use_container_width=True
)


# ============================================================
# SECOND ROW
# ============================================================

col1, col2 = st.columns(2)

# ------------------------------------------------------------
# REVENUE BY PAYMENT METHOD
# ------------------------------------------------------------

with col1:

    payment_sales = (

        df.groupby("Payment_Method")
        ["Total_Amount"]

        .sum()

        .reset_index()
    )

    fig = px.bar(

        payment_sales,

        x="Payment_Method",
        y="Total_Amount",

        color="Total_Amount",

        title="💳 Revenue by Payment Method",

        color_continuous_scale="Blues"
    )

    fig.update_layout(
        coloraxis_showscale=False
    )

    st.plotly_chart(
        apply_sales_theme(fig),
        use_container_width=True
    )


# ------------------------------------------------------------
# SALES CONTRIBUTION TREEMAP
# ------------------------------------------------------------

with col2:

    fig = px.treemap(

        df,

        path=["Category", "Menu_Item"],

        values="Quantity",

        color="Quantity",

        title="🔥 Category & Menu Contribution",

        color_continuous_scale="Plasma"
    )

    st.plotly_chart(
        apply_sales_theme(fig),
        use_container_width=True
    )


# ============================================================
# MONTHLY CATEGORY HEATMAP
# ============================================================

st.subheader("🔥 Category Revenue Heatmap")

heatmap = (

    df.pivot_table(

        index="Category",

        columns="Month",

        values="Total_Amount",

        aggfunc="sum"
    )

    .fillna(0)
)

fig = px.imshow(

    heatmap,

    text_auto=True,

    aspect="auto",

    color_continuous_scale="Viridis"
)

st.plotly_chart(
    apply_sales_theme(fig),
    use_container_width=True
)


# ============================================================
# EXECUTIVE INSIGHTS
# ============================================================

# Find highest earning category

top_category = (

    df.groupby("Category")
    ["Total_Amount"]

    .sum()

    .idxmax()
)

st.markdown("---")

st.info(f"""

### 📌 Executive Insights

🏆 Highest Revenue Category:
**{top_category}**

💰 Total Revenue Generated:
**₹{total_revenue:,.0f}**

💳 Most Preferred Payment Method:
**{top_payment}**

📈 Peak Revenue Day:
**{peak_day_formatted}**

🧾 Average Order Value:
**₹{avg_ticket:,.0f}**

""")