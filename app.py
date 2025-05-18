import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load CSV from GitHub
url = "https://raw.githubusercontent.com/justjames123/raffle-bot/main/discord_message_stats.csv"

@st.cache_data
def load_data():
    return pd.read_csv(url)

# Load & format
df = load_data()

# Columns to display and rename
display_cols = {
    "User": "User",
    "Messages": "Messages",
    "Characters": "Characters",
    "Days in Server": "Days in Server",
    "Final_Tickets_With_Bonus": "Raffle Tickets"
}
df_display = df[list(display_cols.keys())].rename(columns=display_cols)

# Sort by Raffle Tickets by default
df_sorted = df_display.sort_values(by="Raffle Tickets", ascending=False)

# Title
st.markdown("<h1 style='text-align: center;'>🏆 Stellar Blade Discord Server Raffle Leaderboard 🏆</h1>", unsafe_allow_html=True)

# How It Works Dropdown
with st.expander("🎟️ How Raffle Tickets Are Calculated"):
    st.markdown("""
    ## 🎟️ **How It Works**

    Since our goal is to "give back to the community," we're using a raffle system that rewards **meaningful and consistent** engagement in the server. Essentially, the longer and more active you've been in here, the more raffle tickets you get:

    📊 **What Counts:**  
    • Activity is measured from **Feb 1, 2025** (when the PC version was announced)  
    • Both **messages sent** and **characters typed** are counted  
    • Contributions are **normalized by time**, so consistency beats spamming  
    • Max of **5 tickets per day** to prevent abuse  
    • Bonus: **+1 ticket** for every **7 full days** you’ve been in the server  
    • Everyone who reacts to the post gets **at least 1 ticket**
    ---
    """)

    st.markdown("### 🧠 For the Big Brains:")
    st.latex(r'''
    \begin{align*}
    \text{Days} &= \min(\text{days since first message or join date},\ \text{days since Feb\ 1,\ 2025}) \\
    \text{AdjDays} &= \max(\text{Days},\ 21) \\
    \\
    \text{Tickets} &= \min\left(\left(\frac{0.75 \times \text{Messages}}{\text{Days}} + \frac{\text{Characters}}{150 \times \text{Days}}\right),\ \text{Days} \times 5\right) \\
    &\quad + \left\lfloor\frac{\text{Days}}{7}\right\rfloor + 1\ \text{(if no activity)}
    \end{align*}
    ''')

# Filter users
users = df_sorted["User"].unique()
selected_users = st.multiselect("Filter by user(s)", users)

df_filtered = df_sorted[df_sorted["User"].isin(selected_users)] if selected_users else df_sorted

# Sorting option
sort_col = st.selectbox("Sort by", df_filtered.columns, index=df_filtered.columns.get_loc("Raffle Tickets"))
df_filtered = df_filtered.sort_values(by=sort_col, ascending=False)

# Display table without index
st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)

# Chart: Top 10 Raffle Ticket holders
top10 = df_sorted.head(10)
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(top10["User"], top10["Raffle Tickets"])
ax.invert_yaxis()
ax.set_xlabel("Raffle Tickets")
ax.set_title("Top 10 Raffle Ticket Holders")

# Optional value labels
for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.5, bar.get_y() + bar.get_height() / 2, int(width), va='center')

st.pyplot(fig)
