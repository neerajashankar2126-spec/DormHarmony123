import streamlit as st
import pandas as pd

# --- PAGE CONFIG ---
st.set_page_config(page_title="DormHarmony AI", page_icon="📟")

# --- CUSTOM 90s RETRO STYLING ---
st.markdown("""
    <style>
    .main { background-color: #fdfefe; }
    .best-card {
        background-color: #e8f8f5;
        border: 3px solid #27ae60;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 5px 5px 0px #27ae60;
        margin-bottom: 25px;
    }
    .retro-title {
        font-family: 'Courier New', Courier, monospace;
        color: #2e4053;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
# Replace with your 'Published to Web' CSV URL
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQUNeNw8MdyG09A8o2P5K-5eGaTQfC5EpOhfGEKNQ70ZlqtsQd5nAyrdGEeL43cMqeBukEuHiztNhiK/pub?output=csv"

def load_data():
    try:
        # We disable caching so the app stays fresh
        df = pd.read_csv(CSV_URL)
        return df
    except:
        return pd.DataFrame()

df = load_data()

# --- HEADER ---
st.markdown("<h1 class='retro-title'>📟 DormHarmony AI</h1>", unsafe_allow_html=True)
st.caption("Solo AI Project | SRM Institute of Science and Technology")
st.write("---")

# --- USER INPUT SIDEBAR ---
with st.sidebar:
    st.header("🎚️ Your Preferences")
    u_name = st.text_input("Full Name", value="Neeraja")
    
    s1 = st.slider("Sleep (Early -> Late)", 1, 5, 3)
    s2 = st.slider("Cleanliness (Messy -> Neat)", 1, 5, 3)
    s3 = st.slider("Noise (Quiet -> Loud)", 1, 5, 3)
    s4 = st.slider("Social (Introvert -> Extrovert)", 1, 5, 3)
    s5 = st.slider("AC (Low -> High)", 1, 5, 3)
    s6 = st.slider("Share (No Guests -> Guests)", 1, 5, 3)
    s7 = st.slider("Lights (Dark -> Bright)", 1, 5, 3)
    s8 = st.radio("Smoker?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No", horizontal=True)

# --- MATCHING LOGIC ---
if st.button("🚀 Calculate State-Space Matches"):
    if df.empty:
        st.error("Database connection failed. Check your CSV URL.")
    else:
        user_vals = [s1, s2, s3, s4, s5, s6, s7]
        results = []

        for index, row in df.iterrows():
            # Hard Constraint Check
            if s8 != row['Smoke']:
                continue
            
            # Manhattan Distance Calculation
            db_vals = [row['Sleep'], row['Cleanliness'], row['Noise'], row['Social'], row['AC'], row['Share'], row['Lights']]
            diff = sum(abs(u - d) for u, d in zip(user_vals, db_vals))
            
            # Score out of 100% (28 is max possible difference)
            score = round((1 - (diff / 28)) * 100, 1)
            
            if score > 0:
                results.append({"name": row['Name'], "score": score})
        
        # Sort results by highest score
        results = sorted(results, key=lambda x: x['score'], reverse=True)

        if not results:
            st.warning("No compatible roommates found in the current pool.")
        else:
            # 🏆 HIGHLIGHT BEST MATCH
            st.subheader("⭐ Top Match Found")
            best = results[0]
            st.markdown(f"""
                <div class="best-card">
                    <h2 style='margin:0; color:#145a32;'>{best['name']}</h2>
                    <p style='font-size:1.2em;'>Compatibility Score: <b>{best['score']}%</b></p>
                    <p style='color:#566573; font-style:italic;'>This candidate is your mathematically ideal roommate based on Manhattan Distance heuristic.</p>
                </div>
            """, unsafe_allow_html=True)

            # 📋 SHOW OTHER OPTIONS
            if len(results) > 1:
                st.write("### Other Potential Matches")
                for other in results[1:]:
                    col_name, col_progress = st.columns([1, 2])
                    with col_name:
                        st.write(f"**{other['name']}**")
                    with col_progress:
                        st.progress(int(other['score']))
                        st.caption(f"Match: {other['score']}%")
