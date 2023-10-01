import os

import streamlit as st
import pandas as pd
import numpy as np
from pages.custom_module.st_main import (
    MyStSessionState
    , Page, PageColumnSelection, PageLoad, PageSave, PageDataFrameDisplay
)

class PivotTableApp:
    def __init__(self, df: pd.DataFrame, cols_measure: list):
        self.ss = MyStSessionState()
        self.df = df
        
        # session stateで状態を初期化
        if 'df' not in self.ss:
            self.ss.df = df
        if 'selected_rows' not in self.ss:
            self.ss.selected_rows = []
        if 'selected_cols' not in self.ss:
            self.ss.selected_cols = []
        if 'selected_value' not in self.ss:
            self.ss.selected_value = None
            
        self.ss.cols_measure = list(set(df.columns) & set(cols_measure))
        self.pages = {
            "Load Data": PageLoad(self),
            "Column Selection": PageColumnSelection(self),
            "DataFrame Display": PageDataFrameDisplay(self),            
            "Save": PageSave(self)
        }
        
    def display(self):
        #st.write("### Original Data", self.ss.df.head())
        st.write("#### No more Tableau")
        
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