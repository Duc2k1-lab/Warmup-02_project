# Netflix Data Science Project 



## Cấu trúc
- `notebooks/EDA.ipynb` — notebook EDA
- `notebooks/Training.ipynb` — notebook training + lưu model
- `app_streamlit.py` — web demo Streamlit
- `models/` — nơi lưu model

## Cách chạy
1. Cài đặt thư viện:
```
pip install -r requirements.txt
```

2. Chạy notebook training để tạo model:
```
jupyter notebook notebooks/Training.ipynb
```

3. Chạy web demo:
```
streamlit run app_streamlit.py
```

## Deploy Streamlit free
- Tạo repo GitHub, push code lên.
- Vào Streamlit Community Cloud (free), kết nối repo.
- Đặt entrypoint là `app_streamlit.py`.
