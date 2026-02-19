import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

np.random.seed(42)

df = pd.DataFrame({
    'Date': pd.date_range(start='2024-01-01', periods=200),
    'Category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Sports'], 200),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], 200),
    'Sales': np.random.randint(100, 1000, 200),
    'Profit': np.random.randint(20, 300, 200),
    'Customers': np.random.randint(1, 20, 200)
})

st.set_page_config(layout="wide")
st.title("📊 Interactive Sales Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", df["Sales"].sum())
col2.metric("Total Profit", df["Profit"].sum())
col3.metric("Total Customers", df["Customers"].sum())

fig = px.line(df, x="Date", y="Sales", color="Category",
              title="Sales Trend")
st.plotly_chart(fig, use_container_width=True)
