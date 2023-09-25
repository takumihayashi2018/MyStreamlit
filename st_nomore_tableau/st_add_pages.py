import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ダミーデータを生成
df = pd.DataFrame({
    'A': np.random.rand(100),
    'B': np.random.rand(100)
})

# タブのリスト
tabs = ["棒グラフ", "散布図", "ヒストグラム"]

# ユーザーがタブを選択できるラジオボタン
selected_tab = st.radio("グラフタイプを選択:", tabs)

# 選択したタブに応じて異なるグラフを表示
if selected_tab == "棒グラフ":
    st.bar_chart(df)
elif selected_tab == "散布図":
    fig, ax = plt.subplots()
    ax.scatter(df['A'], df['B'])
    st.pyplot(fig)
else:
    fig, ax = plt.subplots()
    ax.hist(df['A'], bins=20, alpha=0.5, label='A')
    ax.hist(df['B'], bins=20, alpha=0.5, label='B')
    ax.set_title("ヒストグラム")
    ax.legend(loc="upper right")
    st.pyplot(fig)
