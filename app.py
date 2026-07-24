import pandas as pd
import streamlit as st

# Configure page layout
st.set_page_config(
    page_title="YLFC Financial Dashboard", page_icon="💰", layout="wide"
)

st.title("💰 YLFC Financial Dashboard (2025–2026)")
st.markdown("---")


# Load the cleaned dataset
@st.cache_data
def load_data():
    return pd.read_csv("data/cleaned_transactions.csv")


df = load_data()

# --- KPI METRICS ---
total_income = df["Income"].sum()
total_expense = df["Expense"].sum()
net_balance = total_income - total_expense

col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"${total_income:,.2f}")
col2.metric("Total Expense", f"${total_expense:,.2f}")
col3.metric("Net Balance", f"${net_balance:,.2f}")

st.markdown("---")

# --- DATA TABLE ---
st.subheader("📋 Detailed Transaction Logs")
# Note: Updated to Streamlit's latest width setting
st.dataframe(df, width="stretch")