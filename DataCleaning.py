# import pandas as pd
# file_path = "data/Transations of YLFC for 2025-2026 AY.csv"

# print("--- Loading Data ---")
# df = pd.read_csv(file_path)

# print("\n--- FIRST 5 ROWS ---")
# print(df.head())

# print("\n--- DATASET INFO ---")
# print(df.info())

# print("\n--- MISSING VALUES ---")
# print(df.isnull().sum())

# null_count = df["Categories"].isnull().sum()
# print(f"Total missing values in Categories: {null_count}")

# null_rows = df[df["Categories"].isnull()]

# print("\n--- Rows with Missing Categories ---")
# print(null_rows)

# print(list(df.columns))

# print(df[["Income", "Expense"]].describe)

# print(df[["Income", "Expense"]].isnull().sum())

# print(df[["Income", "Expense"]].head(10))

# import pandas as pd

# # 1. Load the dataset
# file_path = "data/Transations of YLFC for 2025-2026 AY.csv"
# df = pd.read_csv(file_path)

# # 2. Clean 'Income' column: remove $ and commas, then convert to numeric
# df["Income"] = (
#     df["Income"]
#     .astype(str)
#     .str.replace("$", "", regex=False)
#     .str.replace(",", "", regex=False)
#     .str.strip()
# )
# df["Income"] = pd.to_numeric(df["Income"], errors="coerce").fillna(0)

# # 3. Clean 'Expense' column: remove $ and commas, then convert to numeric
# df["Expense"] = (
#     df["Expense"]
#     .astype(str)
#     .str.replace("$", "", regex=False)
#     .str.replace(",", "", regex=False)
#     .str.strip()
# )
# df["Expense"] = pd.to_numeric(df["Expense"], errors="coerce").fillna(0)

# # 4. Now calculate totals safely
# total_income = df["Income"].sum()
# total_expense = df["Expense"].sum()
# net_balance = total_income - total_expense

# # 5. Output results
# print("--- FINANCIAL SUMMARY ---")
# print(f"Total Income:  ${total_income:,.2f}")
# print(f"Total Expense: ${total_expense:,.2f}")
# print(f"Net Balance:   ${net_balance:,.2f}")

import pandas as pd

# Load raw dataset
file_path = "data/Transations of YLFC for 2025-2026 AY.csv"
df = pd.read_csv(file_path)

# 1. Clean Income & Expense numeric values
for col in ["Income", "Expense"]:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# 2. Convert Date column to datetime format
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# 3. Fill missing Category values with a placeholder
if "Category" in df.columns:
    df["Category"] = df["Category"].fillna("Uncategorized")

# 4. Export cleaned dataset
output_path = "data/cleaned_transactions.csv"
df.to_csv(output_path, index=False)

print("✅ Data cleaning complete!")
print(f"📁 Saved cleaned dataset to: {output_path}")

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="YLFC Financial Dashboard", page_icon="💰", layout="wide"
)

st.title("💰 YLFC Financial Dashboard (2025–2026)")
st.markdown("---")


@st.cache_data
def load_data():
    return pd.read_csv("data/cleaned_transactions.csv")


df = load_data()

# KPI Metrics
total_income = df["Income"].sum()
total_expense = df["Expense"].sum()
net_balance = total_income - total_expense

col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"${total_income:,.2f}")
col2.metric("Total Expense", f"${total_expense:,.2f}")
col3.metric("Net Balance", f"${net_balance:,.2f}")

st.markdown("---")

# Data Table
st.subheader("📋 Detailed Transaction Logs")
st.dataframe(df, use_container_width=True)