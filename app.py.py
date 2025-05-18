import streamlit as st
import pandas as pd

# Load CSV
CSV_PATH = "F:/Python/discord_message_stats.csv"

@st.cache_data
def load_data():
    try:
        return pd.read_csv(CSV_PATH)
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

df = load_data()

st.title("🎉 Raffle Stats Viewer")

if not df.empty:
    users = df["User"].tolist()
    selected_user = st.selectbox("Select a user to view stats:", users)

    if selected_user:
        row = df[df["User"] == selected_user].iloc[0]

        st.markdown(f"### 📊 Stats for `{selected_user}`")
        st.write(f"• **Messages**: {row['Messages']}")
        st.write(f"• **Characters**: {row['Characters']}")
        st.write(f"• **Days in Server**: {row['Days in Server']}")
        st.write(f"• **Total Tickets**: {row.get('Final_Tickets_With_Bonus', 'N/A')}")

else:
    st.warning("Upload or generate the CSV file first.")
