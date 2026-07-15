import pandas as pd
import streamlit as st

from services.data_loader import DataLoader
from services.profiler import DataProfiler

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="InsightAI",
    page_icon="📊",
    layout="wide",
)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("📊 InsightAI")
st.subheader("Your AI Business Analyst")

st.write(
    "Upload a business dataset and get AI-powered insights."
)

# --------------------------------------------------
# File Upload
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"],
)

# --------------------------------------------------
# Dataset
# --------------------------------------------------

if uploaded_file is not None:

    df = DataLoader.load_file(uploaded_file)

    st.success("Dataset loaded successfully!")

    st.divider()

    st.subheader("📈 Dataset Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric(
        "Memory (KB)",
        round(df.memory_usage(deep=True).sum() / 1024, 2),
    )

    st.divider()

    st.subheader("� Data Profile")
    profile_summary = DataProfiler.profile(df)
    profile_df = pd.DataFrame(
        {
            "Metric": list(profile_summary.keys()),
            "Value": list(profile_summary.values()),
        }
    )
    st.dataframe(profile_df, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("�👀 Data Preview")

    st.dataframe(df.head(10), use_container_width=True)

    st.divider()

    st.subheader("📋 Column Information")

    info_df = pd.DataFrame(
        {
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str),
        }
    )

    st.dataframe(info_df, use_container_width=True)
