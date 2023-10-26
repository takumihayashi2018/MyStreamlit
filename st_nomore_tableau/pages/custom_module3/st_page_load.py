import pandas as pd
import streamlit as st
from .page import Page

class PageLoad(Page):
    """データの読み込み画面を表示するページ"""
    def __init__(self, app, load_key="xxx"):
        self.app = app
        self.load_key = load_key
 
    def load(self):
        ss = self.app.ss
        uploaded_file = None

        if not hasattr(self, 'uploaded_file'): 
            self.uploaded_file = st.file_uploader(
                "Choose a CSV file"
                , type="csv"
                , key=f"core_{self.load_key}"
            )
        uploaded_file = self.uploaded_file
        
        if uploaded_file:
            ss.df = pd.read_csv(uploaded_file)
            #st.write(df.head())
            ss.cols_measure = st.multiselect(
                "Select Measure Fields", ss.df.columns
            )            
            with st.form("load"):
                if st.form_submit_button("load"):
                    setattr(ss, self.load_key, [ss.df, ss.cols_measure])
                    ss.ls_load_keys.add(self.load_key)

    

    def display(self):
        ss = self.app.ss
        
        self.load()
        
        if self.load_key in ss:
            myobj = getattr(ss, self.load_key)
            st.write(myobj[0])


    def xxx(self):
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


