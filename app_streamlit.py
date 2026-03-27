import re
import joblib
import pandas as pd
import streamlit as st

MODEL_PATH = "models/netflix_type_model.joblib"

st.set_page_config(page_title="Netflix Type Predictor", layout="wide")
st.title("Netflix Type Predictor")
st.write("Dự đoán nội dung là Movie hay TV Show dựa trên các thông tin cơ bản.")

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

st.sidebar.header("Nhập thông tin")
release_year = st.sidebar.number_input("Release year", min_value=1950, max_value=2025, value=2020)
rating = st.sidebar.text_input("Rating (VD: PG-13, TV-MA)", value="PG-13")
country_main = st.sidebar.text_input("Country (VD: United States)", value="United States")
main_genre = st.sidebar.text_input("Main genre (VD: Comedies)", value="Comedies")
duration_input = st.sidebar.text_input("Duration (VD: 90 min hoặc 2 Seasons)", value="90 min")


def parse_duration_to_minutes(duration):
    if duration is None:
        return None
    duration = str(duration).strip().lower()
    match = re.search(r"(\d+)", duration)
    if not match:
        return None
    value = int(match.group(1))
    if "season" in duration:
        return value * 60
    return value

if st.sidebar.button("Predict"):
    duration_num = parse_duration_to_minutes(duration_input)
    input_df = pd.DataFrame([
        {
            "release_year": release_year,
            "rating": rating,
            "duration_num": duration_num,
            "country_main": country_main,
            "main_genre": main_genre,
        }
    ])

    prediction = model.predict(input_df)[0]
    st.subheader("Kết quả dự đoán")
    st.success(f"Dự đoán: {prediction}")

st.markdown("---")
st.markdown("### Gợi ý")
st.write("cần chạy notebook training trước để tạo model trong thư mục `models/`.")
