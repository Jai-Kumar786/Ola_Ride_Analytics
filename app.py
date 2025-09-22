import streamlit as st
import pandas as pd
import sqlite3
import os
import dashboard_plots as dp  # Import our final plotting functions

# --- Page Configuration ---
st.set_page_config(
    page_title="Ola Ride Insights Dashboard",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Database Connection & Query Functions ---
@st.cache_resource
def get_db_connection():
    conn = sqlite3.connect('data/ola_analytics.db.sql', check_same_thread=False)
    return conn

@st.cache_data
def run_query(query):
    conn = get_db_connection()
    return pd.read_sql_query(query, conn)

# --- Data Loading for Dashboard ---
@st.cache_data
def load_full_data():
    """Loads the enhanced dataset and prepares it for the dashboard."""
    df = pd.read_csv('data/ola_data_enhanced.csv')
    df['booking_timestamp'] = pd.to_datetime(df['booking_timestamp'])
    return df

full_df = load_full_data()


# --- Main Application ---
st.title("🚕 Ola Ride Insights Dashboard")
st.markdown("An interactive dashboard for exploring and analyzing OLA's ride-sharing data.")

# --- Using Tabs for a Cleaner UI ---
tab1, tab2 = st.tabs(["📊 SQL Query Explorer", "📈 Interactive Dashboard"])

# --- Tab 1: SQL Query Explorer (Unchanged) ---
with tab1:
    st.header("SQL Query Explorer")
    st.markdown("Select a pre-defined business question from the sidebar to see the corresponding data and SQL query.")
    st.sidebar.header("Query Controls")
    sql_files_path = 'sql_queries/'
    try:
        sql_files = sorted([f for f in os.listdir(sql_files_path) if f.endswith('.sql')])
        query_options = {
            f.split('_', 1)[1].replace('_', ' ').replace('.sql', '').title(): f
            for f in sql_files
        }
        selected_query_name = st.sidebar.selectbox(
            "Select a Business Question:",
            options=list(query_options.keys())
        )
        if selected_query_name:
            filename = query_options[selected_query_name]
            filepath = os.path.join(sql_files_path, filename)
            with open(filepath, 'r') as f:
                sql_query = f.read()
            st.subheader(f"Results for: {selected_query_name}")
            result_df = run_query(sql_query)
            st.dataframe(result_df, use_container_width=True)
            with st.expander("View SQL Query"):
                st.code(sql_query, language='sql')
    except Exception as e:
        st.error(f"An error occurred: {e}")


# --- Tab 2: Interactive Dashboard with Plotly ---
with tab2:
    st.header("Dashboard Overview")

    # --- Section 1: KPIs & Overall Performance ---
    st.subheader("Key Performance Indicators (KPIs)")
    kpis = dp.plot_kpi_metrics(full_df)
    cols = st.columns(4)
    cols[0].metric("Total Bookings", kpis["Total Bookings"])
    cols[1].metric("Total Revenue (INR)", kpis["Total Revenue (INR)"])
    cols[2].metric("Average Rating", kpis["Average Rating"])
    cols[3].metric("Success Rate", kpis["Success Rate"])

    st.divider()

    # --- Section 2: Temporal & Status Analysis ---
    st.subheader("Temporal & Booking Status Analysis")
    cols = st.columns(2)
    with cols[0]:
        st.plotly_chart(dp.plot_bookings_over_time(full_df), use_container_width=True)
    with cols[1]:
        st.plotly_chart(dp.plot_booking_status_pie(full_df), use_container_width=True)

    st.divider()

    # --- Section 3: Cancellation Deep Dive ---
    st.subheader("Cancellation Analysis")
    fig_cust_reasons, fig_driver_reasons = dp.plot_cancellation_reasons(full_df)
    cols = st.columns([2, 1, 1]) # Make the hourly chart wider
    with cols[0]:
        st.plotly_chart(dp.plot_cancellations_by_hour(full_df), use_container_width=True)
    with cols[1]:
        st.plotly_chart(fig_cust_reasons, use_container_width=True)
    with cols[2]:
        st.plotly_chart(fig_driver_reasons, use_container_width=True)

    st.divider()

    # --- Section 4: Revenue & Service Quality ---
    st.subheader("Revenue and Service Quality Analysis")
    cols = st.columns(2)
    with cols[0]:
        st.plotly_chart(dp.plot_revenue_by_payment_method(full_df), use_container_width=True)
    with cols[1]:
        st.plotly_chart(dp.plot_ratings_by_vehicle_type(full_df), use_container_width=True)

    st.info("💡 **Tip:** Hover over the charts to see detailed data points. You can also click and drag to zoom in on specific areas.")

