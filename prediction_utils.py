import streamlit as st
import pandas as pd
import joblib
import shap
from streamlit_shap import st_shap


# --- Load Model and Preprocessing Objects ---
@st.cache_resource
def load_prediction_assets():
    """Loads the saved model and the scaler object."""
    try:
        model = joblib.load('models/cancellation_model.joblib')
        scaler = joblib.load('models/scaler.joblib')
    except FileNotFoundError as e:
        st.error(f"Required model asset not found: {e}. Please ensure the training notebooks have been run.")
        return None, None
    return model, scaler


# --- Main Function to Build the Prediction Page ---
def show_prediction_page():
    """Creates the UI for the live prediction page."""
    st.header("Live Cancellation Risk Predictor")
    st.markdown("Enter the details of a hypothetical ride to get a real-time prediction of its cancellation risk.")

    model, scaler = load_prediction_assets()
    if model is None or scaler is None:
        return

    # --- Build the User Interface with Input Widgets ---
    st.subheader("Ride Details")
    col1, col2, col3 = st.columns(3)

    with col1:
        v_tat = st.slider("Vehicle Wait Time (V_TAT in secs)", 0, 310, 170)
        c_tat = st.slider("Customer Wait Time (C_TAT in secs)", 0, 150, 85)
        booking_value = st.number_input("Booking Value (INR)", min_value=100, max_value=10000, value=550)

    with col2:
        ride_distance = st.number_input("Ride Distance (km)", min_value=0, max_value=50, value=15)
        hour_of_day = st.slider("Hour of Day (24h)", 0, 23, 18)
        vehicle_type = st.selectbox("Vehicle Type",
                                    ['Auto', 'Bike', 'Mini', 'Prime Plus', 'Prime Sedan', 'Prime SUV', 'eBike'])
    with col3:
        payment_method = st.selectbox("Payment Method",
                                      ['Cash', 'Credit Card', 'Debit Card', 'UPI'])

    # --- Make Prediction on Button Click ---
    if st.button("Predict Cancellation Risk", type="primary"):
        input_data = pd.DataFrame({
            'v_tat': [v_tat], 'c_tat': [c_tat], 'booking_value': [booking_value],
            'ride_distance': [ride_distance], 'hour_of_day': [hour_of_day],
            'vehicle_type': [vehicle_type], 'payment_method': [payment_method]
        })

        input_data_encoded = pd.get_dummies(input_data)
        train_cols = model.feature_names_in_
        input_data_aligned = input_data_encoded.reindex(columns=train_cols, fill_value=0)

        # Scale the data using the LOADED scaler
        scaled_data_array = scaler.transform(input_data_aligned)

        # --- FIX: Convert scaled array back to DataFrame with correct column names ---
        input_data_scaled = pd.DataFrame(scaled_data_array, columns=train_cols)

        # Make the prediction on the SCALED data
        prediction_proba = model.predict_proba(input_data_scaled)[0][1]

        st.subheader("Prediction Result")
        if prediction_proba > 0.7:
            st.error(f"High Risk of Cancellation: {prediction_proba:.0%}")
        elif prediction_proba > 0.4:
            st.warning(f"Moderate Risk of Cancellation: {prediction_proba:.0%}")
        else:
            st.success(f"Low Risk of Cancellation: {prediction_proba:.0%}")



