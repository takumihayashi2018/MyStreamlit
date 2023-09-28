import os

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
            st.write("Selected Columns:", ", ".join(ss.selected_cols) if ss.selected_cols else "None")
            st.write("Selected Value:", ss.selected_value)
    
            # ss.selected_colsが空の場合
            if not ss.selected_cols:
                grouped_df = self.app.df.groupby(ss.selected_rows).agg({ss.selected_value: np.sum}).reset_index()
                st.write(grouped_df)
                return
    
            if ss.selected_rows and ss.selected_cols and ss.selected_value:
                pivot_table = pd.pivot_table(self.app.df, values=ss.selected_value, index=ss.selected_rows, columns=ss.selected_cols, aggfunc=np.sum)
    
                if pivot_table.columns.nlevels > 1:
                    pivot_table.columns = ['_'.join(map(str, col)) for col in pivot_table.columns.values]
    
                st.write(pivot_table)
            else:
                st.write("Please select both Row and Column fields and a Value field to generate Pivot Table.")


class LoadDataPage(Page):
    """データの読み込み画面を表示するページ"""
    def __init__(self, app):
        self.app = app

    def display(self):
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file:
            self.app.df = pd.read_csv(uploaded_file)
            st.write("Uploaded Data", self.app.df.head())
        else:
            # ここで既存のuser_dataを読み込むコードも追加できます。
            pass


class SavePage(Page):
    """設定したパラメータを保存するページ"""
    def __init__(self, app):
        self.app = app

    def display(self):
        save_path = st.text_input("Specify the save path:")
        if save_path:
            if os.path.exists(os.path.dirname(save_path)) or os.path.dirname(save_path) == '':
                self.app.df.to_csv(save_path, index=False)
                st.success(f"Saved to {save_path}")
            else:
                st.error("The specified directory does not exist.")


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
            "DataFrame Display": DataFrameDisplayPage(self),
            "Load Data": LoadDataPage(self),
            "Save": SavePage(self)
        }
        
    def display(self):
        st.write("## Original Data", self.df.head())
        
        # ラジオボタンでページを選択
        page_name = st.radio("Choose a page:", list(self.pages.keys()))

        # 選択されたページを表示
        page = self.pages[page_name]
        page.display()

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