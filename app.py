import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------
# App Title and Configuration
# ------------------------------
st.set_page_config(page_title="Data Visualization Tool", layout="wide")
st.title("📊 My Data Visualization Tool")
st.write("Upload your dataset (CSV, Excel, or JSON) and explore it through interactive visualizations!")

# ------------------------------
# File Upload Section
# ------------------------------
file = st.file_uploader("📁 Upload a file", type=["csv", "xlsx", "xls", "json"])

if file:
    file_name = file.name

    # Detect file type and read data
    try:
        if file_name.endswith(".csv"):
            df = pd.read_csv(file)
        elif file_name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file)
        elif file_name.endswith(".json"):
            df = pd.read_json(file)
        else:
            st.error("❌ Unsupported file type! Please upload CSV, Excel, or JSON.")
            st.stop()

        st.success(f"✅ Successfully loaded *{file_name}*")

        # ------------------------------
        # Data Preview
        # ------------------------------
        st.subheader("📋 Preview of Data")
        st.write(df.head())

        # Optional summary
        if st.checkbox("Show Dataset Summary"):
            st.write(df.describe())

        # ------------------------------
        # Chart Controls
        # ------------------------------
        st.subheader("🎨 Create Visualization")

        col1, col2, col3 = st.columns(3)

        with col1:
            chart_type = st.selectbox("Select Chart Type", ["Scatter Plot", "Line Chart", "Bar Chart", "Histogram", "Box Plot"])
        with col2:
            x = st.selectbox("Choose X-axis", df.columns)
        with col3:
            y = st.selectbox("Choose Y-axis", df.columns)

        # ------------------------------
        # Filtering Option
        # ------------------------------
        if st.checkbox("Enable Filtering"):
            column_to_filter = st.selectbox("Select column to filter", df.columns)
            unique_values = df[column_to_filter].unique()
            selected_value = st.selectbox("Select value", unique_values)
            df = df[df[column_to_filter] == selected_value]

        # ------------------------------
        # Generate Chart
        # ------------------------------
        if chart_type == "Scatter Plot":
            fig = px.scatter(df, x=x, y=y, title=f"{x} vs {y}", color_discrete_sequence=['#FF6F61'])
        elif chart_type == "Line Chart":
            fig = px.line(df, x=x, y=y, title=f"{x} vs {y}", markers=True)
        elif chart_type == "Bar Chart":
            fig = px.bar(df, x=x, y=y, title=f"{x} vs {y}")
        elif chart_type == "Histogram":
            fig = px.histogram(df, x=x, title=f"Histogram of {x}")
        else:
            fig = px.box(df, x=x, y=y, title=f"Box Plot of {y} by {x}")

        st.plotly_chart(fig, use_container_width=True)

        # ------------------------------
        # Footer
        # ------------------------------
        st.markdown("---")
        st.markdown("<p style='text-align:center;'>Data Visualization Tool</p>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"⚠ Error reading file: {e}")

else:
    st.info("👆 Please upload a CSV, Excel, or JSON file to get started.")

# ------------------------------
# Light Styling
# ------------------------------
st.markdown("""
    <style>
        .stApp {
            background-color: #f9f9f9;
        }
        .stPlotlyChart {
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)