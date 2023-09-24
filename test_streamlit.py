import streamlit as st
import pandas as pd

st.title("Streamlit デモ")

st.write("DataFrameを表示する：")

# ダミーデータを作成
df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [10, 20, 30, 40]
})

st.write(df)
