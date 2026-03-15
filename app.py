import streamlit as st
import pandas as pd

# 1. SETTINGS
st.set_page_config(page_title="DormHarmony", page_icon="🏠")

# 2. DATA LOADING (The Fail-Proof Way)
# PASTE YOUR PUBLISHED CSV URL INSIDE THE QUOTES BELOW
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQUNeNw8MdyG09A8o2P5K-5eGaTQfC5EpOhfGEKNQ70ZlqtsQd5nAyrdGEeL43cMqeBukEuHiztNhiK/pub?output=csv"

def load_data():
    try:
        # We add a random query param to force the browser to get fresh data
        df = pd.read_csv(CSV_URL)
        return df
    except Exception as e:
        st.error("Could not connect to the database. Make sure you 'Published to Web' as CSV!")
        return pd.DataFrame()

df = load_data()

# 3. UI
st.title("📟 DormHarmony AI")
st.write("---")

# User Input
u_name = st.text_input("Your Name")
c1, c2 = st.columns(2)
with c1:
    s1 = st.slider("Sleep", 1, 5, 3)
    s2 = st.slider("Cleanliness", 1, 5, 3)
    s3 = st.slider("Noise", 1, 5, 3)
    s4 = st.slider("Social", 1, 5, 3)
with c2:
    s5 = st.slider("AC", 1, 5, 3)
    s6 = st.slider("Share", 1, 5, 3)
    s7 = st.slider("Lights", 1, 5, 3)
    s8 = st.radio("Smoke?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

# 4. MATCHING LOGIC
if st.button("🚀 Find Matches"):
    if df.empty:
        st.warning("Database is empty or not connected.")
    else:
        st.subheader("Results")
        user_vals = [s1, s2, s3, s4, s5, s6, s7]
        
        # Manhattan Distance Calculation
        for index, row in df.iterrows():
            # Hard Constraint: Smoke
            if s8 != row['Smoke']:
                continue
            
            # Distance
            db_vals = [row['Sleep'], row['Cleanliness'], row['Noise'], row['Social'], row['AC'], row['Share'], row['Lights']]
            diff = sum(abs(u - d) for u, d in zip(user_vals, db_vals))
            score = round((1 - (diff / 28)) * 100, 1)
            
            if score > 0:
                st.write(f"**{row['Name']}**: {score}% Match")
                st.progress(int(score))

st.write("---")
st.caption("SRM KTR Solo Project | Neeraja")
