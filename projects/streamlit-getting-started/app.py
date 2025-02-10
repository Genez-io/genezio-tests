import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Streamlit Demo",
    page_icon="📊",
    layout="wide"
)

# Main title
st.title("📊 Demo Dashboard")
st.markdown("---")

# Sidebar with controls
with st.sidebar:
    st.header("Configuration")
    
    # Slider for number of rows
    num_rows = st.slider("Number of rows", 10, 100, 50)
    
    # Chart type selector
    chart_type = st.selectbox(
        "Chart type",
        ["Line", "Bar", "Scatter"]
    )

# Generate demo data
df = pd.DataFrame({
    'Date': pd.date_range('2024-01-01', periods=num_rows),
    'Sales': np.random.randint(100, 1000, num_rows),
    'Profit': np.random.normal(500, 150, num_rows)
})

# Display data in two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Raw Data")
    st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("Statistics")
    st.write("Sales statistics:")
    st.write(f"- Mean: {df['Sales'].mean():.2f}")
    st.write(f"- Max: {df['Sales'].max()}")
    st.write(f"- Min: {df['Sales'].min()}")

# Data visualization
st.subheader("Visualization")

if chart_type == "Line":
    fig = px.line(df, x='Date', y=['Sales', 'Profit'])
elif chart_type == "Bar":
    fig = px.bar(df, x='Date', y='Sales')
else:
    fig = px.scatter(df, x='Sales', y='Profit', trendline="ols")

st.plotly_chart(fig, use_container_width=True)

# Interactive widget
if st.button("Generate new data"):
    st.rerun()

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Genezio and Streamlit")