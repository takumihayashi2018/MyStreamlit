import streamlit as st
import pandas as pd
import numpy as np

# 初期データフレームと計算式の辞書の設定
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        'A': [1, 2, 3, 4],
        'B': [5, 6, 7, 8]
    })
if "formulas" not in st.session_state:
    st.session_state.formulas = {}

# カラム操作のフォームを作成
with st.form(key='column_operations'):
    
    # 新しいカラムを追加
    new_column_name = st.text_input("Enter new column name:")
    lambda_expression = st.text_input("Enter lambda expression (use 'x' for the dataframe and 'np' for numpy):", "x['A'] + np.sin(x['B'])")
    
    # カラムを削除
    delete_column_name = st.selectbox("Choose a column to delete:", ["None"] + list(st.session_state.df.columns))
    
    # フォームの送信ボタン
    submitted = st.form_submit_button("Apply Changes")

    # フォームが送信されたら処理を実行
    if submitted:
        # 新しいカラムを追加
        if new_column_name:
            try:
                st.session_state.df[new_column_name] = st.session_state.df.apply(lambda x: eval(lambda_expression, {"np": np, "x": x}), axis=1)
                st.session_state.formulas[new_column_name] = lambda_expression
                st.write(f"Added new column '{new_column_name}'")
            except Exception as e:
                st.write(f"Error: {e}")
        
        # カラムを削除
        if delete_column_name != "None" and delete_column_name in st.session_state.df.columns:
            del st.session_state.df[delete_column_name]
            if delete_column_name in st.session_state.formulas:
                del st.session_state.formulas[delete_column_name]
            st.write(f"Deleted column '{delete_column_name}'")

# 計算式確認のフォーム
with st.form(key='formula_check'):
    selected_column = st.selectbox("Choose a column to check its formula:", list(st.session_state.df.columns))
    submit_check = st.form_submit_button("Check Formula")
    
    if submit_check and selected_column in st.session_state.formulas:
        st.write(f"Formula for '{selected_column}': {st.session_state.formulas[selected_column]}")

# 常に更新されたDataFrameを表示
st.write("DataFrame:")
st.write(st.session_state.df)
