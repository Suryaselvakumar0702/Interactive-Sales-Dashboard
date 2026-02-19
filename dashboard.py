import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Interactive Sales Dashboard", layout="wide")

# Load Dataset
@st.cache_data
def load_data():
    return pd.read_csv("sales_data.csv", parse_dates=["Date"])

df = load_data()

st.title("📊 Interactive Sales Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")
selected_region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

selected_product = st.sidebar.multiselect(
    "Select Product",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)

filtered_df = df[
    (df["Region"].isin(selected_region)) &
    (df["Product"].isin(selected_product))
]

# KPI Section
col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"₹ {filtered_df['Total_Sales'].sum():,.0f}")
col2.metric("Total Quantity Sold", filtered_df["Quantity"].sum())
col3.metric("Average Price", f"₹ {filtered_df['Price'].mean():,.0f}")

st.markdown("---")

# 1️⃣ Sales Trend (Plotly Line Chart)
st.subheader("📈 Sales Trend Over Time")
sales_trend = filtered_df.groupby("Date")["Total_Sales"].sum().reset_index()
fig_line = px.line(sales_trend, x="Date", y="Total_Sales",
                   title="Daily Sales Trend", markers=True)
st.plotly_chart(fig_line, use_container_width=True)

# 2️⃣ Sales by Product (Bar Chart)
st.subheader("📦 Sales by Product")
product_sales = filtered_df.groupby("Product")["Total_Sales"].sum().reset_index()
fig_bar = px.bar(product_sales, x="Product", y="Total_Sales",
                 color="Product", title="Total Sales per Product")
st.plotly_chart(fig_bar, use_container_width=True)

# 3️⃣ Sales Distribution (Seaborn Boxplot)
st.subheader("📊 Sales Distribution by Product")
plt.figure(figsize=(8, 5))
sns.boxplot(data=filtered_df, x="Product", y="Total_Sales")
plt.xticks(rotation=45)
st.pyplot(plt)

# 4️⃣ Correlation Heatmap (Seaborn)
st.subheader("🔥 Correlation Heatmap")
corr = filtered_df[["Quantity", "Price", "Total_Sales"]].corr()
plt.figure(figsize=(6, 4))
sns.heatmap(corr, annot=True, cmap="coolwarm")
st.pyplot(plt)

# 5️⃣ Regional Sales (Plotly Pie Chart)
st.subheader("🌍 Regional Sales Distribution")
region_sales = filtered_df.groupby("Region")["Total_Sales"].sum().reset_index()
fig_pie = px.pie(region_sales, values="Total_Sales", names="Region",
                 title="Sales by Region")
st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")
st.success("Dashboard Loaded Successfully ✅")
