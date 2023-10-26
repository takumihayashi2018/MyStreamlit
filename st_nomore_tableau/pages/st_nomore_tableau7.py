import os

import streamlit as st
import pandas as pd
import numpy as np
from pages.custom_module3.st_main import (
    MyStSessionState
    , Page, PageColumnSelection, PageLoad, PageSave, PageDataFrameDisplay, PagePagesLoad, PageEtl
)
ss0 = st.session_state

class PivotTableApp:
    def __init__(self, df: pd.DataFrame, cols_measure: list):
        
        if not hasattr(ss0, 'ss'):
            ss0.ss = MyStSessionState(
                ls_load_keys = set()
                , page_name_cur = None
                , df=df
                , selected_rows=[]
                , selected_cols = []
                , selected_value = None
                , cols_measure = list(set(df.columns) & set(cols_measure))
            )
            self.ss = ss0.ss
        else:
            self.ss = ss0.ss
            
        #self.df = df
        #self.ss.cols_measure = list(set(df.columns) & set(cols_measure))
        self.pages = {
            #"Load Data": PageLoad(self),
            "PagePagesLoad": PagePagesLoad(self),
            "ETL" : PageEtl(self),
            "Column Selection": PageColumnSelection(self),
            "DataFrame Display": PageDataFrameDisplay(self),            
            "Save": PageSave(self)
        }
        
    def move_next_prev_page(self, col):
        """ページのナビゲーションを処理するメソッド"""
        # ページのリストを取得
        page_list = list(self.pages.keys())

        # session_stateに現在のページのインデックスを保存
        if "current_page_index" not in st.session_state:
            st.session_state.current_page_index = 0

        # 前のボタンを追加
        if col.button("Previous"):
            # インデックスを減少させて前のページを表示
            st.session_state.current_page_index = (st.session_state.current_page_index - 1) % len(page_list)
            st.experimental_rerun()

        # 次のボタンを追加
        if col.button("Next"):
            # インデックスを増加させて次のページを表示
            st.session_state.current_page_index = (st.session_state.current_page_index + 1) % len(page_list)
            st.experimental_rerun()

        # 選択されたページ名を返す
        return page_list[st.session_state.current_page_index]

    def display(self):
        st.write("#### No more Tableau")
        ss = self.ss
        col1, col2 = st.columns(2)
        page_name_new = self.move_next_prev_page(col1)
        
    
        # ラジオボタンでページを選択（デフォルト値としてページの移動結果を使用）
        page_name = col2.radio("Choose a page:", list(self.pages.keys()), index=list(self.pages.keys()).index(page_name_new))
    
        ss.page_name_cur = page_name

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