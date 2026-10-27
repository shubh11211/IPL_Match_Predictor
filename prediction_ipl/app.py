import streamlit as st 
import pickle
import pandas as pd 

# Unique list of cities and teams
cities = [
    'Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
    'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
    'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
    'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
    'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
    'Sharjah', 'Mohali', 'Bengaluru'
]

teams = [
    'Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
    'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
    'Rajasthan Royals', 'Delhi Capitals'
]

# 1. Use relative pathing for the model file
try:
    pipe = pickle.load(open('/pipe.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model file 'pipe.pkl' not found. Please ensure it's in the same directory.")
    st.stop()

st.title('IPL Match Predictor')

# 2. Prevent UI breakage if image is missing
try:
    st.image('prediction_ipl/ipl.jpg', use_container_width=True)
except:
    pass

col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams), index=0)
with col2:
    # 3. Prevent user from picking identical teams
    available_bowling_teams = [team for team in teams if team != batting_team]
    bowling_team = st.selectbox('Select the bowling team', sorted(available_bowling_teams), index=0)

selected_city = st.selectbox('Hosting City', sorted(cities))
target = st.number_input('Target Score', min_value=0, value=150, step=1)

col3, col4, col5 = st.columns(3)
with col3:
    score = st.number_input('Current Score', min_value=0, value=0, step=1)
with col4:
    overs = st.number_input('Overs Bowled', min_value=0.0, max_value=20.0, value=0.0, step=0.1)
with col5:
    wickets = st.number_input('Wickets Down', min_value=0, max_value=10, value=0, step=1)

if st.button('Predict Win Probability'):
    # Basic structural math adjustments
    runs_left = target - score
    balls_left = int((20 - overs) * 6)
    wickets_left = 10 - wickets

    # 4. Zero-Division Handling for Current Run Rate (CRR)
    if overs > 0:
        crr = score / overs 
    else:
        crr = 0.0

    # 5. Zero-Division & Target Edge Case Handling for Required Run Rate (RRR)
    if balls_left > 0:
        rrr = (runs_left * 6) / balls_left
    else:
        rrr = 0.0 if runs_left <= 0 else 99.9  # High placeholder if balls end but runs remain

    # Match state business logic checks before passing to model
    if score >= target:
        st.success(f"🎉 {batting_team} has already won the match!")
    elif wickets >= 10:
        st.error(f"❌ All out! {bowling_team} wins the match.")
    elif overs > 20:
        st.error("❌ Match over! Overs exceeded 20.")
    else:
        # Build payload
        input_df = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [selected_city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [wickets_left],
            'total_runs_x': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

        # Run inference
        result = pipe.predict_proba(input_df)
        lose = result[0][0]
        win = result[0][1]

        # Display results cleanly
        st.subheader("Win Probability Breakdown")
        st.progress(float(win))
        
        c1, c2 = st.columns(2)
        c1.metric(label=f"🏏 {batting_team} Win %", value=f"{round(win * 100)}%")
        c2.metric(label=f"🥎 {bowling_team} Win %", value=f"{round(lose * 100)}%")
