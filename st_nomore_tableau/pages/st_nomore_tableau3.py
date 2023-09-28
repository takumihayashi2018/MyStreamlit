import streamlit as st
import pandas as pd
import numpy as np
from pages.custom_module.my_st_session_state import MyStSessionState

class Page:
    """ページのベースクラス"""
    def display(self):
        raise NotImplementedError()

class ColumnSelectionPage(Page):
    """カラム選択画面を表示するページ"""
    def __init__(self, app):
        self.app = app

    def display(self):
        ss = self.app.ss  # MyStSessionStateインスタンスを参照
        cols = st.columns(3)
        cols_key = [ col for col in list(self.app.df.columns) if col not in self.app.cols_measure ]
        with cols[0]:
            ss.selected_rows = st.multiselect("Select Row Fields", cols_key , ss.selected_rows)
        with cols[1]:
            ss.selected_cols = st.multiselect("Select Column Fields", cols_key, ss.selected_cols)
        with cols[2]:
            ss.selected_value = st.selectbox("Select Values Field", self.app.cols_measure, index=self.app.cols_measure.index(ss.selected_value) if ss.selected_value else 0)

class DataFrameDisplayPage(Page):
    """データフレーム表示画面を表示するページ"""
    def __init__(self, app):
        self.app = app

    def display(self):
        ss = self.app.ss  # MyStSessionStateインスタンスを参照
        st.write("Selected Rows:", ", ".join(ss.selected_rows))
        st.write("Selected Columns:", ", ".join(ss.selected_cols))
        st.write("Selected Value:", ss.selected_value)

        if ss.selected_rows and ss.selected_cols and ss.selected_value:
            pivot_table = pd.pivot_table(self.app.df, values=ss.selected_value, index=ss.selected_rows, columns=ss.selected_cols, aggfunc=np.sum)

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
        self.ss = MyStSessionState()

        # session stateで状態を初期化
        if 'selected_rows' not in self.ss:
            self.ss.selected_rows = []
        if 'selected_cols' not in self.ss:
            self.ss.selected_cols = []
        if 'selected_value' not in self.ss:
            self.ss.selected_value = None
            
        self.cols_measure = list(set(df.columns) & set(cols_measure))
        self.pages = {
            "Column Selection": ColumnSelectionPage(self),
            "DataFrame Display": DataFrameDisplayPage(self)
        }

    def display(self):
        st.write("## Original Data", self.df.head())
        
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
