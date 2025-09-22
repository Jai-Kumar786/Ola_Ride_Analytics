import pandas as pd
import plotly.express as px

# Set a default theme for a professional look
px.defaults.template = "plotly_white"

# --- Charting Functions ---

def plot_kpi_metrics(df):
    """
    Calculates KPI metrics for display in Streamlit.
    """
    total_bookings = df['booking_id'].nunique()
    successful_rides_df = df[df['booking_status'] == 'Success']
    total_revenue = successful_rides_df['booking_value'].sum()
    avg_rating = df['customer_rating'].mean()
    success_rate = (len(successful_rides_df) / total_bookings) * 100 if total_bookings > 0 else 0

    return {
        "Total Bookings": f"{total_bookings:,}",
        "Total Revenue (INR)": f"₹{total_revenue:,.0f}",
        "Average Rating": f"{avg_rating:.2f} ⭐",
        "Success Rate": f"{success_rate:.1f}%"
    }


def plot_bookings_over_time(df):
    """Creates an interactive line chart of bookings over time."""
    daily_bookings = df.resample('D', on='booking_timestamp').size().reset_index(name='count')
    fig = px.line(
        daily_bookings, x='booking_timestamp', y='count', title='Booking Volume Over Time',
        labels={'booking_timestamp': 'Date', 'count': 'Number of Bookings'}
    )
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig


def plot_booking_status_pie(df):
    """Creates an interactive donut chart for booking status breakdown."""
    status_counts = df['booking_status'].value_counts().reset_index()
    fig = px.pie(
        status_counts, names='booking_status', values='count', title='Booking Status Breakdown', hole=0.4
    )
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig


def plot_cancellations_by_hour(df):
    """Creates an interactive bar chart of cancellations by hour."""
    cancelled_df = df[df['booking_status'].str.contains('Canceled')]
    hourly_cancellations = cancelled_df['hour_of_day'].value_counts().sort_index().reset_index()
    fig = px.bar(
        hourly_cancellations, x='hour_of_day', y='count', title='Cancellations by Hour of the Day',
        labels={'hour_of_day': 'Hour of Day (24h)', 'count': 'Number of Cancellations'}
    )
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig


def plot_cancellation_reasons(df):
    """Creates separate bar charts for customer and driver cancellation reasons."""
    cust_cancel_df = df[df['booking_status'] == 'Canceled by Customer']
    driver_cancel_df = df[df['booking_status'] == 'Canceled by Driver']
    cust_reasons = cust_cancel_df['cancellation_reason'].value_counts().nlargest(5).reset_index()
    driver_reasons = driver_cancel_df['cancellation_reason'].value_counts().nlargest(5).reset_index()

    fig_cust = px.bar(cust_reasons, y='cancellation_reason', x='count', orientation='h', title='Top 5 Customer Reasons')
    fig_cust.update_layout(margin=dict(l=20, r=20, t=40, b=20), yaxis={'categoryorder':'total ascending', 'title':''})

    fig_driver = px.bar(driver_reasons, y='cancellation_reason', x='count', orientation='h', title='Top 5 Driver Reasons')
    fig_driver.update_layout(margin=dict(l=20, r=20, t=40, b=20), yaxis={'categoryorder':'total ascending', 'title':''})

    return fig_cust, fig_driver


def plot_revenue_by_payment_method(df):
    """Creates an interactive bar chart of revenue by payment method."""
    successful_rides = df[df['booking_status'] == 'Success']
    revenue_by_method = successful_rides.groupby('payment_method')['booking_value'].sum().sort_values().reset_index()
    fig = px.bar(
        revenue_by_method, y='payment_method', x='booking_value', orientation='h', title='Revenue by Payment Method',
        labels={'booking_value': 'Total Revenue (INR)', 'payment_method': 'Payment Method'}
    )
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), yaxis={'title':''})
    return fig


def plot_ratings_by_vehicle_type(df):
    """Creates an interactive box plot to show rating distributions by vehicle type."""
    fig = px.box(
        df.dropna(subset=['customer_rating']),  # Drop nulls for this plot
        x='vehicle_type',
        y='customer_rating',
        title='Customer Rating Distribution by Vehicle Type',
        labels={'vehicle_type': 'Vehicle Type', 'customer_rating': 'Customer Rating'}
    )
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig

