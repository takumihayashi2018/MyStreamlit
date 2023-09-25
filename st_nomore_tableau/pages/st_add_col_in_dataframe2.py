import streamlit as st
import pandas as pd

# 初期データフレーム
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame({
        'A': [1, 2, 3, 4],
        'B': [5, 6, 7, 8]
    })

st.write("DataFrame:")
st.write(st.session_state.df)

# 新しいカラムを追加
new_column_name = st.text_input("Enter new column name:")
lambda_expression = st.text_input("Enter lambda expression (use 'x' for the dataframe):", "x['A'] + x['B']")
if st.button("Add Column"):
    try:
        st.session_state.df[new_column_name] = st.session_state.df.apply(lambda x: eval(lambda_expression), axis=1)
        st.write(f"Added new column '{new_column_name}'")
    except Exception as e:
        st.write(f"Error: {e}")

# カラムを削除
delete_column_name = st.selectbox("Choose a column to delete:", st.session_state.df.columns)
if st.button("Delete Column"):
    del st.session_state.df[delete_column_name]
    st.write(f"Deleted column '{delete_column_name}'")
