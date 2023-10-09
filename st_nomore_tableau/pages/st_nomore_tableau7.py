import os

import streamlit as st
import pandas as pd
import numpy as np
from pages.custom_module3.st_main import (
    MyStSessionState
    , Page, PageColumnSelection, PageLoad, PageSave, PageDataFrameDisplay, PagePagesLoad
)

class PivotTableApp:
    def __init__(self, df: pd.DataFrame, cols_measure: list):
        self.ss = MyStSessionState(
            df=df
            , selected_rows=[]
            , selected_cols = []
            , selected_value = None
            , cols_measure = list(set(df.columns) & set(cols_measure))
        )
        self.df = df
        #self.ss.cols_measure = list(set(df.columns) & set(cols_measure))
        self.pages = {
            "Load Data": PageLoad(self),
            "PagePagesLoad": PagePagesLoad(self),
            "Column Selection": PageColumnSelection(self),
            "DataFrame Display": PageDataFrameDisplay(self),            
            "Save": PageSave(self)
        }
        
    def display(self):
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
        'XXX': np.random.random(100) * 1000,
        'YYY': np.random.random(100) * 500
    })

    app = PivotTableApp(df, ["XXX", "YYY"])
    app.display()