import streamlit as st
import pandas as pd
import numpy as np

class Page:
    """ページのベースクラス"""
    def display(self):
        raise NotImplementedError()

class ColumnSelectionPage(Page):
    """カラム選択画面を表示するページ"""
    def __init__(self, app):
        self.app = app

    def display(self):
        cols = st.columns(3)
        with cols[0]:
            st.session_state.selected_rows = st.multiselect("Select Row Fields", list(self.app.df.columns), st.session_state.selected_rows)
        with cols[1]:
            st.session_state.selected_cols = st.multiselect("Select Column Fields", list(self.app.df.columns), st.session_state.selected_cols)
        with cols[2]:
            st.session_state.selected_value = st.selectbox("Select Values Field", self.app.cols_measure, index=self.app.cols_measure.index(st.session_state.selected_value) if st.session_state.selected_value else 0)

class DataFrameDisplayPage(Page):
    """データフレーム表示画面を表示するページ"""
    def __init__(self, app):
        self.app = app

    def display(self):
        st.write("Selected Rows:", ", ".join(st.session_state.selected_rows))
        st.write("Selected Columns:", ", ".join(st.session_state.selected_cols))
        st.write("Selected Value:", st.session_state.selected_value)

        if st.session_state.selected_rows and st.session_state.selected_cols and st.session_state.selected_value:
            pivot_table = pd.pivot_table(self.app.df, values=st.session_state.selected_value, index=st.session_state.selected_rows, columns=st.session_state.selected_cols, aggfunc=np.sum)

            if pivot_table.columns.nlevels > 1:
                pivot_table.columns = ['_'.join(map(str, col)) for col in pivot_table.columns.values]

            st.write(pivot_table)

        # コメントボックス
        user_comment = st.text_area("Leave your comment here:")
        if user_comment:
            st.write("Your Comment:", user_comment)
        else:
            st.write("Please select both Row and Column fields and a Value field to generate Pivot Table.")

class PivotTableApp:
    def __init__(self, df: pd.DataFrame, cols_measure: list):
        self.df = df

        # session stateで状態を初期化
        if 'selected_rows' not in st.session_state:
            st.session_state.selected_rows = []
        if 'selected_cols' not in st.session_state:
            st.session_state.selected_cols = []
        if 'selected_value' not in st.session_state:
            st.session_state.selected_value = None
            
        self.cols_measure = list(set(df.columns) & set(cols_measure))
        self.pages = {
            "Column Selection": ColumnSelectionPage(self),
            "DataFrame Display": DataFrameDisplayPage(self)
        }
        
    def display(self):
        st.write("## Original Data", self.df)
        
        # ラジオボタンでページを選択
        page_name = st.radio("Choose a page:", list(self.pages.keys()))

        # 選択されたページを表示
        page = self.pages[page_name]
        page.display()

# 以下はデモ用のコード
if __name__ == "__main__":
    df = pd.DataFrame({
        'Date': pd.date_range(start='2021-01-01', periods=100, freq='D'),
        'Category': np.random.choice(['A', 'B', 'C'], 100),
        'sub_category': np.random.choice(['X', 'Y', 'Z'], 100),
        'Value': np.random.randint(1, 100, 100),
        'RWA': np.random.random(100) * 1000,
        'EAD': np.random.random(100) * 500
    })

    app = PivotTableApp(df, ["RWA", "EAD"])
    app.display()
