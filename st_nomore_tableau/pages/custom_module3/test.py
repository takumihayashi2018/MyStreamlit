import pandas as pd
import streamlit as st
from .page import Page

class PageLoad(Page):
    """データの読み込み画面を表示するページ"""
    def __init__(self, app, load_name, file_types=["csv"], read_methods=None):
        self.app = app
        self.load_name = load_name
        self.file_types = file_types
        self.read_methods = read_methods or {
            "csv": pd.read_csv,
            # 他のファイルタイプの読み込み方法もここに追加できます。
        }
        self.ss = self.app.ss
        self.df_load_data = pd.DataFrame()
        self.cols_measure = []
        self.uploaded_file = None
        setattr(self.ss, load_name, [self.df_load_data, self.cols_measure, self.uploaded_file])

    def load(self, uploaded_file):
        file_extension = uploaded_file.name.split('.')[-1]
        read_method = self.read_methods.get(file_extension)

        if read_method:
            df = read_method(uploaded_file)
            df = df.copy()
            setattr(self.ss, self.load_name, [df, [], None])
        else:
            st.warning(f"Unsupported file type: {file_extension}")

    def display_uploaded_data(self):
        load_attr = getattr(self.ss, self.load_name)
        df = load_attr[0]
        cols_measure = st.multiselect("Select Measure Fields", df.columns)
        load_attr[1] = cols_measure
        st.write("Uploaded Data", df.head())

    def display(self):
        load_attr = getattr(self.ss, self.load_name)
        btn_click_file_upload = False

        with st.form("for file upload"):
            uploaded_file = st.file_uploader("Choose a file", type=self.file_types)
            btn_click_file_upload = st.form_submit_button("ok")

            if btn_click_file_upload:
                st.write("hello")
                self.uploaded_file = uploaded_file
                load_attr[2] = self.uploaded_file
                if self.uploaded_file:
                    self.load(self.uploaded_file)

        btn_click_set_cols_measure = False
        with st.form("for set_cols_measure"):
            self.display_uploaded_data()
            btn_click_set_cols_measure = st.form_submit_button("set_cols_measure")
