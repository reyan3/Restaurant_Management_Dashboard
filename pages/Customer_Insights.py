# Import required libraries
import streamlit as st           # Used to build the dashboard UI
import plotly.express as px      # Used for interactive charts

# Import custom functions
from utils.load_data import load_data
from utils.filters import sidebar_filters


# ============================================================
# LOAD DATA
# ============================================================

st.set_page_config(
    page_title="Customer Insight",
    page_icon="🍽️",
    layout="wide"
)

# Load the dataset from Excel
df = load_data()

# Apply sidebar filters selected by the user
df = sidebar_filters(df)

# If no records remain after filtering, stop execution
if df.empty:
    st.warning("⚠️ No data available for selected filters.")
    st.stop()


# ============================================================
# PAGE HEADER
# ============================================================

# Create a styled banner/header using HTML + CSS
st.markdown("""
<div style='
    padding:25px;
    border-radius:20px;
    background:linear-gradient(135deg,#111827,#1E293B);
    border:1px solid rgba(255,255,255,0.08);
'>

<h1 style='color:white;'>👥 Customer Intelligence</h1>

<p style='color:#94A3B8;font-size:18px;'>
Analyze customer behavior, loyalty, satisfaction,
and spending patterns.
</p>

</div>
""", unsafe_allow_html=True)

# Add some vertical spacing
st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# KPI CALCULATIONS
# ============================================================

# Count unique customers
# Example: CUST001, CUST002...
total_customers = df["Customer_ID"].nunique()


# Calculate average customer rating
# Example: (4 + 5 + 3 + 4) / 4
avg_rating = round(df["Rating"].mean(), 1)


# Calculate average spending per customer

# Step 1:
# Group data by customer

# Step 2:
# Sum total amount spent by each customer

# Step 3:
# Find average spending across all customers

avg_spending = round(
    df.groupby("Customer_ID")["Total_Amount"]
      .sum()
      .mean(),
    0
)


# Count repeat customers

# value_counts() counts orders per customer

# gt(1) checks if customer placed more than one order

# sum() counts how many True values exist

repeat_customers = (
    df["Customer_ID"]
    .value_counts()
    .gt(1)
    .sum()
)


# ============================================================
# DISPLAY KPI CARDS
# ============================================================

# Create 4 equal columns
c1, c2, c3, c4 = st.columns(4)

# Display metrics inside columns
c1.metric("👥 Customers", f"{total_customers:,}")

c2.metric(
    "💰 Avg Spending",
    f"₹{avg_spending:,.0f}"
)

c3.metric(
    "🔁 Repeat Customers",
    repeat_customers
)

c4.metric(
    "⭐ Avg Rating",
    avg_rating
)

# Horizontal divider
st.markdown("---")


# ============================================================
# TOP CUSTOMERS CHART
# ============================================================

# Group customers and calculate total revenue generated

customer_sales = (
    df.groupby("Customer_Name")["Total_Amount"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

# Create horizontal bar chart

fig = px.bar(
    customer_sales,

    # Revenue on x-axis
    x="Total_Amount",

    # Customer names on y-axis
    y="Customer_Name",

    orientation="h",

    # Color bars based on revenue
    color="Total_Amount",

    color_continuous_scale="Viridis",

    title="🏆 Top 10 Customers by Revenue"
)

fig.update_layout(
    template="plotly_dark",

    # Sort bars properly
    yaxis={'categoryorder': 'total ascending'},

    coloraxis_showscale=False
)

# Display chart
st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# SECOND ROW OF CHARTS
# ============================================================

col1, col2 = st.columns(2)


# ------------------------------------------------------------
# CUSTOMER RATING DISTRIBUTION
# ------------------------------------------------------------

with col1:

    # Histogram shows frequency of ratings

    fig = px.histogram(
        df,

        # Ratings on x-axis
        x="Rating",

        # Number of bins
        nbins=5,

        title="⭐ Customer Rating Distribution",

        color_discrete_sequence=["#00E676"]
    )

    fig.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ------------------------------------------------------------
# ORDER FREQUENCY DISTRIBUTION
# ------------------------------------------------------------

with col2:

    # Count total orders placed by each customer

    customer_orders = (
        df.groupby("Customer_Name")
          .size()
          .reset_index(name="Orders")
    )

    # Show how many customers placed
    # 1 order, 2 orders, 3 orders etc.

    fig = px.histogram(
        customer_orders,

        x="Orders",

        nbins=20,

        title="🛒 Order Frequency Distribution",

        color_discrete_sequence=["#42A5F5"]
    )

    fig.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# CUSTOMER SEGMENTATION
# ============================================================

# Create customer summary table

customer_segment = (

    df.groupby("Customer_Name")

    .agg({

        # Total money spent
        "Total_Amount": "sum",

        # Total orders placed
        "Order_ID": "count"

    })

    .reset_index()
)

# Rename column for readability

customer_segment.rename(
    columns={
        "Order_ID": "Total_Orders"
    },

    inplace=True
)

# Scatter plot to segment customers

fig = px.scatter(

    customer_segment,

    # Number of orders
    x="Total_Orders",

    # Total spending
    y="Total_Amount",

    # Bubble size
    size="Total_Amount",

    hover_name="Customer_Name",

    title="🎯 Customer Segmentation",

    color="Total_Amount",

    color_continuous_scale="Turbo"
)

fig.update_layout(
    template="plotly_dark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

st.subheader("📌 Executive Summary")

# Get highest spending customer

best_customer = customer_sales.iloc[0]["Customer_Name"]

# Display important business insights

st.info(f"""
🏆 Highest Revenue Customer: **{best_customer}**

👥 Total Unique Customers: **{total_customers:,}**

⭐ Average Satisfaction Score: **{avg_rating}/5**

💰 Average Customer Spending: **₹{avg_spending:,.0f}**
""")