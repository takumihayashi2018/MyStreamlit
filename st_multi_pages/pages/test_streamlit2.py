import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Streamlit 機能のデモ")

# スライダー
num_samples = st.slider("サンプル数の選択", 1, 1000, 100)

# ダミーデータ生成
data = pd.DataFrame({
    'x': np.linspace(0, 10, num_samples),
    'y': np.sin(np.linspace(0, 10, num_samples))
})

# チェックボックス
show_data = st.checkbox("データを表示")

if show_data:
    st.write(data)

# プロット
st.write("sin波のグラフ")
fig, ax = plt.subplots()
ax.plot(data['x'], data['y'])
ax.set_xlabel('x')
ax.set_ylabel('y')
st.pyplot(fig)
