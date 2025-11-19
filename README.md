IPL Match Win Predictor

Predicts the probability of a team winning an IPL match based on the live match situation using machine learning and ball-by-ball data.
 Overview
This project uses historical IPL deliveries and matches data to build a real-time win-probability prediction system.
It processes ball-by-ball records, engineers match-situation features, trains an ML model, and provides a clean Streamlit web app to interact with the model.

🔧 Features Used
The model takes the following live match conditions as input:
Batting team
Bowling team
City
Runs left
Balls left
Wickets remaining
Current score
Current run rate (CRR)
Required run rate (RRR)


These features were engineered from raw match and delivery datasets.

🧠 How the Model Works

Data from matches.csv and deliveries.csv is cleaned and merged.

Feature engineering is applied (runs left, balls left, crr, rrr, wickets, etc.).

A machine learning model is trained (Logistic Regression / Random Forest — depending on what you used).

The trained model (saved as model.pkl) is loaded in a Streamlit UI for live predictions.



Install dependencies:
pandas
numpy
sklearn
streamlit 


Run the Streamlit web app:
streamlit run app.py



Cross-validated results included in notebook


🛠 Tech Stack


Python


Pandas, NumPy


Scikit-learn


Streamlit (Frontend UI)


Matplotlib / Seaborn


Jupyter Notebook for analysis



🔮 Future Improvements


Deploy on Streamlit Cloud / Render


Add better algorithms (XGBoost, CatBoost)


Include match-visualization graphs


Use live match APIs for real-time predictions


