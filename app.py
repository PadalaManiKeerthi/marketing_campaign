import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Marketing Campaign Dashboard", layout="wide")
st.title("📊 Customer Segmentation - Marketing Campaign")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('segmented_customers.csv')

df = load_data()

# Sidebar filter
st.sidebar.header("Filter Customers")
segments = st.sidebar.multiselect(
    "Select Segment", 
    options=df['Segment'].unique(), 
    default=df['Segment'].unique()
)
filtered_df = df[df['Segment'].isin(segments)]

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", len(filtered_df))
col2.metric("Avg Recency", f"{filtered_df['Recency'].mean():.0f} days")
col3.metric("Avg Spending", f"${filtered_df['Total_Spending'].mean():.0f}")
col4.metric("Avg Income", f"${filtered_df['Income'].mean():.0f}")

st.divider()

# Charts
col_left, col_right = st.columns(2)
with col_left:
    fig1 = px.pie(filtered_df, names='Segment', title='Customer Segments Distribution', hole=0.3)
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    avg_spend = filtered_df.groupby('Segment')['Total_Spending'].mean().reset_index()
    fig2 = px.bar(avg_spend, x='Segment', y='Total_Spending', color='Segment', title='Average Spending by Segment')
    st.plotly_chart(fig2, use_container_width=True)

fig3 = px.scatter(filtered_df, x='Recency', y='Total_Spending', color='Segment', size='Income', hover_data=['ID'], title='Recency vs Spending')
st.plotly_chart(fig3, use_container_width=True)

# Table
st.subheader("Customer Data")
st.dataframe(filtered_df, use_container_width=True)
