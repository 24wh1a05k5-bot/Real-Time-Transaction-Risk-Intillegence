import streamlit as st
import requests
import random
import time
import pandas as pd

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Fraud Intelligence Dashboard",
    layout="wide"
)

# ------------------ STYLE ------------------
st.markdown("""
<style>
.card {
    padding: 20px;
    border-radius: 15px;
    background: #161b22;
    box-shadow: 0 4px 12px rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.title("💳 Real-Time Fraud Intelligence Dashboard")
st.markdown("Live transaction monitoring with dynamic risk scoring")

# ------------------ PLACEHOLDERS ------------------
chart_placeholder = st.empty()
table_placeholder = st.empty()
alert_placeholder = st.empty()

# ------------------ DATA STORAGE ------------------
data = []
result = {}

# ------------------ START BUTTON ------------------
if st.button("▶ Start Simulation"):

    for i in range(20):

        amount = random.randint(100, 10000)
        frequency = random.randint(1, 10)

        txn = {
            "amount": amount,
            "frequency": frequency
        }

        try:
            res = requests.post(
                "http://127.0.0.1:8000/predict",
                json=txn
            )

            if res.status_code != 200:
                st.error(f"API Error: {res.status_code}")
                break

            result = res.json()

            risk = result.get("risk_score", 0)
            decision = result.get("decision", "UNKNOWN")

            data.append({
                "Transaction": i + 1,
                "Amount": amount,
                "Frequency": frequency,
                "Risk Score": risk,
                "Decision": decision
            })

            df = pd.DataFrame(data)

            # ------------------ CHART ------------------
            chart_placeholder.line_chart(df["Risk Score"])

            # ------------------ TABLE ------------------
            table_placeholder.dataframe(
                df.tail(10),
                use_container_width=True
            )

            # ------------------ ALERTS ------------------
            if decision == "BLOCK":
                alert_placeholder.error(
                    f"🚨 Fraud Detected! Transaction {i+1}"
                )

            elif decision == "REVIEW":
                alert_placeholder.warning(
                    f"⚠️ Suspicious Transaction! Transaction {i+1}"
                )

            else:
                alert_placeholder.success(
                    f"✅ Safe Transaction {i+1}"
                )

            time.sleep(1)

        except Exception as e:
            st.error(f"API not reachable: {e}")
            break

    # ------------------ REASONS ------------------
    st.markdown("## 🧠 Why this Decision?")

    reasons = result.get("reasons", [])

    if reasons:
        for reason in reasons:
            st.markdown(f"- {reason}")
    else:
        st.info("No significant risk factors detected.")

else:
    st.info("Click 'Start Simulation' to begin monitoring transactions.")