
import pandas as pd
import plotly.express as px
import streamlit as st

# Configure page layout
st.set_page_config(
    page_title="YLFC Financial Dashboard", page_icon="💰", layout="wide"
)

st.title("YLFC Financial Dashboard (2025–2026)")
st.markdown("---")


# Load the cleaned dataset
@st.cache_data
def load_data():
    data = pd.read_csv("data/Transations of YLFC for 2025-2026 AY.csv")
    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    return data


df = load_data()

# Identify categorical grouping columns available in your dataset
group_columns = [
    col
    for col in [
        "Under_Categories",
        "Categories",
        "2nd_Under_Categories",
        "Who",
    ]
    if col in df.columns
]

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filter Options")

# 1. Category Filter
selected_under_cat = []
if "Under_Categories" in df.columns:
    all_under_cats = sorted(
        df["Under_Categories"].dropna().unique().tolist()
    )
    selected_under_cat = st.sidebar.multiselect(
        "Select Under Categories:",
        options=all_under_cats,
        default=all_under_cats,
    )

# 2. Date Range Filter
date_range = []
if "Date" in df.columns and not df["Date"].isnull().all():
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()

    date_range = st.sidebar.date_input(
        "Select Date Range:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

# --- APPLY FILTERS ---
filtered_df = df.copy()

if "Under_Categories" in df.columns and selected_under_cat:
    filtered_df = filtered_df[
        filtered_df["Under_Categories"].isin(selected_under_cat)
    ]

if "Date" in df.columns and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["Date"].dt.date >= start_date)
        & (filtered_df["Date"].dt.date <= end_date)
    ]

# --- KPI METRICS ---
total_income = filtered_df["Income"].sum()
total_expense = filtered_df["Expense"].sum()
net_balance = total_income - total_expense

col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"${total_income:,.2f}")
col2.metric("Total Expense", f"${total_expense:,.2f}")
col3.metric("Net Balance", f"${net_balance:,.2f}")

st.markdown("---")

# --- INTERACTIVE VISUALIZATIONS SECTION ---
st.subheader("📊 Dynamic Visual Analytics")

# Dropdown allowing user to adjust which column drives the charts
if group_columns:
    selected_group_col = st.selectbox(
        "🎯 Choose Column to Analyze Charts By:",
        options=group_columns,
        index=0,
    )
else:
    selected_group_col = None

chart_col1, chart_col2 = st.columns(2)

# Chart 1: Income vs Expense Overview Pie Chart
with chart_col1:
    st.markdown("### 🥧 Overall Cash Flow")
    summary_df = pd.DataFrame(
        {
            "Type": ["Income", "Expense"],
            "Amount": [total_income, total_expense],
        }
    )
    fig_pie = px.pie(
        summary_df,
        names="Type",
        values="Amount",
        color="Type",
        color_discrete_map={"Income": "#2ca02c", "Expense": "#d62728"},
        hole=0.4,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Chart 2: Dynamic Distribution Donut Chart
with chart_col2:
    if selected_group_col:
        st.markdown(f"### 🍩 Expense Breakdown by {selected_group_col}")
        expense_by_cat = (
            filtered_df.groupby(selected_group_col)["Expense"]
            .sum()
            .reset_index()
        )
        expense_by_cat = expense_by_cat[expense_by_cat["Expense"] > 0]

        fig_donut = px.pie(
            expense_by_cat,
            names=selected_group_col,
            values="Expense",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("---")

# --- SUMMARY TABLE & ADJUSTABLE BAR CHART ---
if selected_group_col:
    st.subheader(f"📋 Summary Breakdown by {selected_group_col}")

    cat_summary = (
        filtered_df.groupby(selected_group_col)[["Income", "Expense"]]
        .sum()
        .reset_index()
        .sort_values(by="Expense", ascending=False)
    )

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("### 📋 Formatted Summary Table")
        st.dataframe(
            cat_summary.style.format(
                {"Income": "${:,.2f}", "Expense": "${:,.2f}"}
            ),
            width="stretch",
        )

    with col_right:
        st.markdown(f"### 📈 Total Expenses per {selected_group_col}")
        fig_bar = px.bar(
            cat_summary,
            x=selected_group_col,
            y="Expense",
            text_auto=".2s",
            color="Expense",
            color_continuous_scale="Reds",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# --- DATA TABLE ---
st.subheader("📋 Detailed Transaction Logs")
st.dataframe(filtered_df, width="stretch")