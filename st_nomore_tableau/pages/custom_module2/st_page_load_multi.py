''' --- st_page_load  ---'''
import pandas as pd
import streamlit as st
from .page import Page

class PageLoadMulti(Page):
    """データの読み込み画面を表示するページ"""
    def __init__(self, app):
        self.app = app

    def display(self):
        ss = self.app.ss
        ss.doc1 = st.file_uploader("Choose a text file1")
        ss.doc2 = st.file_uploader("Choose a text file2")
        st.write(ss._df_sessions)

        if uploaded_file:
            temporary_df = pd.read_csv(uploaded_file)
            st.write("Preview: ", temporary_df.head())
            

            # Load button
            if st.button('Load'):
                self.app.df = temporary_df
                ss.df = self.app.df
                ls_properties_to_refresh = ['selected_cols', 'selected_rows', 'selected_value']
                ss.refresh(ls_properties_to_refresh)
                st.write(ss._df_sessions)
                st.write("Data Loaded Successfully!")

        else:
            # ここで既存のuser_dataを読み込むコードも追加できます。
            pass





