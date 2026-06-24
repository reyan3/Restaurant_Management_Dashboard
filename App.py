import streamlit as st

# ============================================================
# PAGE SETTINGS
# ============================================================
# Configure the webpage title, icon and layout

st.set_page_config(
    page_title="Restaurant Analytics Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS STYLING
# ============================================================
# Using HTML + CSS to make the dashboard look modern

st.markdown("""
<style>

/* Reduce top spacing */
.block-container {
    padding-top: 1.5rem;
}

/* Header Banner Styling */
.hero-container {
    background: linear-gradient(135deg, #0F172A, #1E293B);
    padding: 2.5rem;
    border-radius: 20px;
    margin-bottom: 2rem;
}

/* Main Title */
.hero-title {
    font-size: 42px;
    font-weight: bold;
    color: white;
}

/* Subtitle */
.hero-subtitle {
    font-size: 16px;
    color: #94A3B8;
}

/* KPI Card Styling */
.landing-metric-card {
    background: rgba(30, 41, 59, 0.4);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    transition: 0.3s;
}

.landing-metric-card:hover {
    transform: translateY(-5px);
    border: 1px solid #00E676;
}

.landing-metric-title {
    color: #94A3B8;
    font-size: 12px;
    text-transform: uppercase;
}

.landing-metric-value {
    color: white;
    font-size: 30px;
    font-weight: bold;
}

/* Information Box Styling */
.guide-container {
    padding: 25px;
    border-radius: 15px;
    margin-top: 30px;
    background: rgba(30, 41, 59, 0.2);
}

.guide-title {
    color: white;
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 15px;
}

.guide-step {
    color: #94A3B8;
    font-size: 15px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR DESIGN
# ============================================================
# Change sidebar background color

st.sidebar.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #0F172A;
}
</style>
""", unsafe_allow_html=True)

# Display dashboard status
st.sidebar.success("✅ Dashboard Ready")

# ============================================================
# HEADER SECTION
# ============================================================
# Main banner displayed at the top

st.markdown("""
<div class='hero-container'>
    <div class='hero-title'>
        🍽️ Restaurant Analytics Dashboard
    </div>
    <div class='hero-subtitle'>
        Monitor sales, customer behavior,
        and payment trends in one place.
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# KPI CARDS SECTION
# ============================================================
# Display important business metrics

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class='landing-metric-card'>
        <div class='landing-metric-title'>
            Today's Revenue
        </div>
        <div class='landing-metric-value'>
            ₹3,56,800
        </div>
        <small style='color:#00E676;'>
            +12% compared to last week
        </small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='landing-metric-card'>
        <div class='landing-metric-title'>
            Occupied Tables
        </div>
        <div class='landing-metric-value'>
            18 / 25
        </div>
        <small style='color:#38BDF8;'>
            Peak dining hours
        </small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='landing-metric-card'>
        <div class='landing-metric-title'>
            Average Service Time
        </div>
        <div class='landing-metric-value'>
            14 mins
        </div>
        <small style='color:#00E676;'>
            2 mins faster than before
        </small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class='landing-metric-card'>
        <div class='landing-metric-title'>
            Customer Rating
        </div>
        <div class='landing-metric-value'>
            4.8 / 5
        </div>
        <small style='color:#00E676;'>
            Excellent customer satisfaction
        </small>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# ABOUT DASHBOARD SECTION
# ============================================================
# Explain how to use the dashboard

st.markdown("""
<div class='guide-container'>
<div class='guide-title'>
📊 How to Use This Dashboard
</div>
<p style='color:#94A3B8;'>

This dashboard helps restaurant owners and managers
analyze sales, customers and payments.

Use the sidebar to explore different sections and apply filters.

</p>
<div class='guide-step'>
1️⃣ Open the sidebar on the left.
</div>
<div class='guide-step'>
2️⃣ Select a page such as Overview, Sales, or Customer Insights.
</div>
<div class='guide-step'>
3️⃣ Apply filters to analyze specific data.
</div>
<div class='guide-step'>
4️⃣ Study charts and insights to make better business decisions.
</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# POP-UP MESSAGE
# ============================================================
# Small notification shown when dashboard loads

st.toast(
    "🚀 Dashboard loaded successfully!",
    icon="✅"
)