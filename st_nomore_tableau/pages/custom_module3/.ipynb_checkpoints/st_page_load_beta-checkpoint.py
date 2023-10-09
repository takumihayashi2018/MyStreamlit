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


import pandas as pd
import streamlit as st
from .page import Page

class PageLoad(Page):
    """データの読み込み画面を表示するページ"""
    def __init__(self, app, file_types=["csv"], read_methods=None):
        self.app = app
        self.file_types = file_types
        self.read_methods = read_methods or {
            "csv": pd.read_csv,
            # 他のファイルタイプの読み込み方法もここに追加できます。
        }

    def load_data(self, uploaded_file, df):
        file_extension = uploaded_file.name.split('.')[-1]
        read_method = self.read_methods.get(file_extension)
        
        if read_method:
            self.app.df = read_method(uploaded_file)
            self.app.ss.df 
            ls_property_names_to_refresh = [
                "selected_rows", "selected_cols", "selected_value"
            ]
            self.app.ss.refresh(ls_property_names_to_refresh)
        else:
            st.warning(f"Unsupported file type: {file_extension}")

    def display_uploaded_data(self):
        self.app.ss.cols_measure = st.multiselect("Select Measure Fields", self.app.ss.df.columns)
        st.write("Uploaded Data", self.app.df.head())

    def display(self):
        uploaded_file = st.file_uploader("Choose a file", type=self.file_types)
        
        if uploaded_file:
            self.load_data(uploaded_file)
            self.display_uploaded_data()
        else:
            # ここで既存のuser_dataを読み込むコードも追加できます。
            pass
