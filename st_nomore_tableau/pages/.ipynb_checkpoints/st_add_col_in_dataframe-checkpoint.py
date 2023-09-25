import streamlit as st
import pandas as pd

# サンプルデータフレーム
df = pd.DataFrame({
    'A': [1, 2, 3, 4],
    'B': [5, 6, 7, 8]
})

st.write("Original DataFrame:")
st.write(df)

# ユーザー入力を取得
new_column_name = st.text_input("Enter new column name:", "C")
lambda_expression = st.text_input("Enter lambda expression (use 'x' for the dataframe):", "x['A'] + x['B']")

if st.button("Add Column"):
    try:
        df[new_column_name] = df.apply(lambda x: eval(lambda_expression), axis=1)
        st.write("Updated DataFrame:")
        st.write(df)
    except Exception as e:
        st.write(f"Error: {e}")
