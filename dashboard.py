import streamlit as st
import pandas as pd
from datetime import datetime
from src.agent import WaterIntakeAgent
from src.database import log_intake, get_intake_history

if "tracker_started" not in st.session_state:
    st.session_state.tracker_started = False

user_id = ""
# Welcome section 

if not st.session_state.tracker_started:
    st.title("Welcome to AI water tracker")
    st.markdown("""
        Track your daily hydration with help of an AI assistant. 
        Log your intake, get smart and stay healthy smartly
""")

    if st.button(" Start tracking"):
        st.session_state.tracker_started = True 
        st.rerun()

else:
    st.title("💧 AI Water Tracker Dashboard")

    # Sidebar: Intake Input
    st.sidebar.header("Log Your Water Intake")
    # --- MODIFICATION START ---
    # Assign the value from the input to the user_id variable
    user_id = st.sidebar.text_input("User ID", value= user_id) # Use the defined user_id as default
    # --- MODIFICATION END ---
    intake_ml = st.sidebar.number_input("Water Intake (ml)", min_value=0, step=100)

    if st.sidebar.button("Submit"):
        if user_id and intake_ml:
            log_intake(user_id, intake_ml)
            st.success(f"✅ Logged {intake_ml}ml for {user_id}")

            agent = WaterIntakeAgent()
            feedback = agent.analyse_intake(intake_ml)
            st.info(f"💡 AI Feedback: {feedback}")

# Divider
st.markdown("---")

# 💧 History Section
st.header("💧 Water Intake History")

# Now user_id is guaranteed to be defined
if user_id:
    history = get_intake_history(user_id)
    if history:
        # Assuming row[1] is the date string, and row[0] is the intake value
        dates = [datetime.strptime(row[1], "%Y-%m-%d") for row in history] # Removed extra space before %Y
        values = [row[0] for row in history]

        df = pd.DataFrame({
            "Date": dates,
            "Water Intake (ml)": values
        })

        st.dataframe(df)
        st.line_chart(df, x="Date", y="Water Intake (ml)")
    else:
        st.warning(f"No water intake data found for user '{user_id}'. Please log your intake first.")
        