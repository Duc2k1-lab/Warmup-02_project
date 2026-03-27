import io

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="Netflix Data Demo", page_icon="🎬", layout="wide")


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    required_cols = ["type", "country", "release_year", "rating"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = None

    clean = pd.DataFrame()
    clean["type"] = df["type"].astype(str).str.strip().replace({"": "Unknown"})
    clean["country"] = df["country"].astype(str).str.strip().replace({"": "unknown", "": "unknown"})
    clean["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")
    clean["rating"] = df["rating"].astype(str).str.strip().replace({"": "Unknown"})

    clean = clean[
        (clean["type"] != "Unknown")
        | (clean["country"] != "unknown")
        | (clean["release_year"].notna())
    ].copy()

    return clean


def top_n(series: pd.Series, n: int) -> pd.Series:
    return series.value_counts().head(n)


def render_dashboard(df: pd.DataFrame) -> None:
    total = len(df)
    movie_count = (df["type"].str.lower() == "movie").sum()
    unique_countries = df["country"].nunique()
    avg_year = df["release_year"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tong ban ghi", f"{total:,}")
    c2.metric("So quoc gia", f"{unique_countries:,}")
    c3.metric("Ty le Movie", f"{(movie_count / total * 100) if total else 0:.1f}%")
    c4.metric("Nam phat hanh TB", f"{avg_year:.0f}" if pd.notna(avg_year) else "N/A")

    type_counts = df["type"].value_counts().reset_index()
    type_counts.columns = ["type", "count"]

    country_counts = top_n(df["country"], 10).reset_index()
    country_counts.columns = ["country", "count"]

    rating_counts = top_n(df["rating"], 10).reset_index()
    rating_counts.columns = ["rating", "count"]

    year_counts = (
        df["release_year"]
        .dropna()
        .astype(int)
        .value_counts()
        .sort_index(ascending=False)
        .head(15)
        .sort_index()
        .reset_index()
    )
    year_counts.columns = ["release_year", "count"]

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.subheader("Phan bo Type")
        st.plotly_chart(
            px.bar(type_counts, x="type", y="count", color="type"),
            use_container_width=True,
        )
    with row1_col2:
        st.subheader("Top 10 Quoc gia")
        st.plotly_chart(
            px.bar(country_counts, x="country", y="count", color="count"),
            use_container_width=True,
        )

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.subheader("Top 10 Rating")
        st.plotly_chart(
            px.bar(rating_counts, x="rating", y="count", color="count"),
            use_container_width=True,
        )
    with row2_col2:
        st.subheader("So luong theo nam (Top 15 nam)")
        st.plotly_chart(
            px.line(year_counts, x="release_year", y="count", markers=True),
            use_container_width=True,
        )


st.title("Netflix Data Demo (Streamlit)")
st.caption("Upload file CSV va xem dashboard KPI + bieu do ngay tren trinh duyet.")

uploaded_file = st.file_uploader("Tai file CSV", type=["csv"])

with st.expander("Hoac dung du lieu mau"):
    if st.button("Nap du lieu mau", use_container_width=True):
        sample_csv = io.StringIO(
            """type,country,release_year,rating
TV Show,Brazil,2020,TV-MA
Movie,India,2008,TV-MA
Movie,Indonesia,2016,TV-PG
Movie,United States,2019,R
TV Show,South Korea,2021,TV-14
Movie,India,2017,TV-14
TV Show,Japan,2018,TV-MA
Movie,United Kingdom,2013,PG-13
Movie,United States,2020,PG-13
TV Show,Brazil,2022,TV-MA
"""
        )
        sample_df = pd.read_csv(sample_csv)
        render_dashboard(normalize_dataframe(sample_df))

if uploaded_file is not None:
    try:
        raw_df = pd.read_csv(uploaded_file)
        clean_df = normalize_dataframe(raw_df)
        if clean_df.empty:
            st.warning("File co du lieu khong hop le hoac thieu cot can thiet.")
        else:
            st.success(f"Da nap {len(clean_df):,} dong du lieu.")
            render_dashboard(clean_df)
    except Exception as exc:
        st.error(f"Khong the doc file CSV: {exc}")
