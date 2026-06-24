import pandas as pd
import streamlit as st

@st.cache_data
def load_data():

    # Read Excel file
    df = pd.read_excel(
        "data/Restaurant_Management_Dataset_5000_Rows.xlsx"
    )

    # ---------------- DATE FEATURES ---------------- #

    df["Order_Date"] = pd.to_datetime(df["Order_Date"])

    df["Year"] = df["Order_Date"].dt.year
    df["Month"] = df["Order_Date"].dt.month_name()
    df["Month_No"] = df["Order_Date"].dt.month
    df["Day"] = df["Order_Date"].dt.day_name()
    df["Day_No"] = df["Order_Date"].dt.day
    df["Weekday"] = df["Order_Date"].dt.weekday
    df["Quarter"] = df["Order_Date"].dt.quarter
    df["Week"] = df["Order_Date"].dt.isocalendar().week

    # ---------------- BUSINESS FEATURES ---------------- #

    # Average order value
    df["Avg_Order_Value"] = (
        df["Total_Amount"] / df["Quantity"]
    ).round(2)

    # Weekend Orders
    df["Is_Weekend"] = df["Day"].isin(
        ["Saturday", "Sunday"]
    )

    # Rating Category
    df["Rating_Category"] = pd.cut(
        df["Rating"],
        bins=[0, 3, 4, 5],
        labels=["Poor", "Good", "Excellent"]
    )

    # Price Segmentation
    df["Price_Category"] = pd.cut(
        df["Price_Per_Item"],
        bins=[0, 5, 10, 100],
        labels=["Low", "Medium", "High"]
    )

    # Sort Months Properly
    month_order = [
        "January", "February", "March",
        "April", "May", "June",
        "July", "August", "September",
        "October", "November", "December"
    ]

    df["Month"] = pd.Categorical(
        df["Month"],
        categories=month_order,
        ordered=True
    )

    return df