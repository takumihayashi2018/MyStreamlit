import pandas as pd
import streamlit as st
from .page import Page

class PageLoad(Page):
    """データの読み込み画面を表示するページ"""
    def __init__(self, app):
        self.app = app

    def display(self):
        ss = self.app.ss
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file:
            self.app.df = pd.read_csv(uploaded_file)
            
            ss.df = self.app.df
            ls_property_names_to_refresh = [
                "selected_rows", "selected_cols", "selected_value"
            ]
            ss.refresh(ls_property_names_to_refresh)
            
        else:
            # ここで既存のuser_dataを読み込むコードも追加できます。
            pass

        ss.cols_measure = st.multiselect("Select Measure Fields", ss.df.columns)
        st.write("Uploaded Data", self.app.df.head())
 