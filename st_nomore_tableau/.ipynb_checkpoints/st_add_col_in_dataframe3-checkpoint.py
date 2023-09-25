import streamlit as st
import pandas as pd
import numpy as np

# 初期データフレームの設定
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        'A': [1, 2, 3, 4],
        'B': [5, 6, 7, 8]
    })

# カラム操作のフォームを作成
with st.form(key='column_operations'):
    
    # 新しいカラムを追加
    new_column_name = st.text_input("Enter new column name:")
    lambda_expression = st.text_input("Enter lambda expression (use 'x' for the dataframe):", "x['A'] + x['B']")
    
    # カラムを削除
    delete_column_name = st.selectbox("Choose a column to delete:", ["None"] + list(st.session_state.df.columns))
    
    # フォームの送信ボタン
    submitted = st.form_submit_button("Apply Changes")

    # フォームが送信されたら処理を実行
    if submitted:
        # 新しいカラムを追加
        if new_column_name:
            try:
                st.session_state.df[new_column_name] = st.session_state.df.apply(lambda x: eval(lambda_expression), axis=1)
                st.write(f"Added new column '{new_column_name}'")
            except Exception as e:
                st.write(f"Error: {e}")
        
        # カラムを削除
        if delete_column_name != "None" and delete_column_name in st.session_state.df.columns:
            del st.session_state.df[delete_column_name]
            st.write(f"Deleted column '{delete_column_name}'")

# 常に更新されたDataFrameを表示
st.write("DataFrame:")
st.write(st.session_state.df)
