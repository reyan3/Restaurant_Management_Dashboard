import streamlit as st
import pandas as pd

def sidebar_filters(df):
    """
    Advanced filter panel for the Restaurant Management System.
    Safely handles temporal processing and multi-variable filtering.
    """
    # Safeguard against empty or missing data structures
    if df.empty:
        st.sidebar.warning("⚠️ No data available to filter.")
        return df

    # --- STYLE & ACCENT OVERRIDES ---
    st.sidebar.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background-color: #0F172A !important;
        }
        .sidebar-header {
            font-size: 20px;
            font-weight: 700;
            color: #FFFFFF;
            letter-spacing: -0.5px;
            margin-bottom: 5px;
        }
        .sidebar-status {
            background: rgba(0, 230, 118, 0.1);
            color: #00E676;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 20px;
            border: 1px solid rgba(0, 230, 118, 0.2);
        }
        </style>
        <div class="sidebar-header">⚙️ Control Panel</div>
        <div class="sidebar-status">● Core System Live</div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # --- TEMPORAL SAFEGUARDING ---
    # Since "Restaurant_Management_Dataset_5000_Rows.xlsx" uses 'Order_Date', 
    # we derive a clean numeric 'Year' attribute if it isn't explicitly provided.
    if "Year" not in df.columns and "Order_Date" in df.columns:
        df["Year"] = pd.to_datetime(df["Order_Date"]).dt.year

    # Fallback to an array of stringified/integer options or default to 'All'
    available_years = sorted(df["Year"].unique()) if "Year" in df.columns else ["All"]
    available_categories = sorted(df["Category"].unique()) if "Category" in df.columns else []
    available_order_types = sorted(df["Order_Type"].unique()) if "Order_Type" in df.columns else []

    # --- FILTER CONFIGURATION ACTION RENDERERS ---
    # Reset Filters Feature - highly requested functionality for busy supervisors
    if st.sidebar.button("🔄 Reset Global Configurations", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    # 1. Year Dimension Filter
    years = st.sidebar.multiselect(
        "📅 Financial Calendar Year",
        options=available_years,
        default=available_years,
        help="Filter data streams by chronological transaction cycles."
    )

    # 2. Category Filter
    categories = st.sidebar.multiselect(
        "🍔 Culinary Category",
        options=available_categories,
        default=available_categories,
        help="Isolate operational trends across menu segments."
    )

    # 3. Order Placement Workflow Filter
    order_type = st.sidebar.multiselect(
        "📦 Fulfillment Channel",
        options=available_order_types,
        default=available_order_types,
        help="Segment performance by counter delivery configurations."
    )

    # --- PIPELINE SEGMENTATION EXECUTION ---
    # Apply conditions iteratively, prioritizing safety defaults if lists get completely emptied by a user
    filtered_df = df.copy()

    if years and "Year" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["Year"].isin(years)]
        
    if categories and "Category" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["Category"].isin(categories)]
        
    if order_type and "Order_Type" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["Order_Type"].isin(order_type)]

    return filtered_df