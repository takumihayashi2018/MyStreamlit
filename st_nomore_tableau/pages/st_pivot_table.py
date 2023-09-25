import streamlit as st
import pandas as pd
import numpy as np

# デモのためのサンプルデータ
def load_data():
    df = pd.DataFrame({
        'Date': pd.date_range(start='2021-01-01', periods=100, freq='D'),
        'Category': np.random.choice(['A', 'B', 'C'], 100),
        'sub_category': np.random.choice(['X', 'Y', 'Z'], 100),
        'Value': np.random.randint(1, 100, 100),
        'RWA': np.random.random(100) * 1000,
        'EAD': np.random.random(100) * 500
    })
    return df

df = load_data()
st.write("## Original Data", df)

# Pivot Tableの作成
st.write("## Pivot Table")
selected_rows = st.multiselect("Select Row Fields", list(df.columns))
selected_cols = st.multiselect("Select Column Fields", list(df.columns))
col_measures = ["RWA", "EAD"]
selected_value = st.selectbox("Select Values Field", col_measures)

if selected_rows and selected_cols and selected_value:
    pivot_table = pd.pivot_table(df, values=selected_value, index=selected_rows, columns=selected_cols, aggfunc=np.sum)
    
    # カラムヘッダーのアンダースコアでの結合
    if pivot_table.columns.nlevels > 1:
        pivot_table.columns = ['_'.join(map(str, col)) for col in pivot_table.columns.values]
    
    st.write(pivot_table)
else:
    st.write("Please select both Row and Column fields and a Value field to generate Pivot Table.")

if __name__ == "__main__":
    pass
