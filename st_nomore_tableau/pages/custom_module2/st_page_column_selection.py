''' --- st_page_column_selection  ---'''
import streamlit as st
from .page import Page

class PageColumnSelection(Page):
    """カラム選択画面を表示するページ"""
    def __init__(self, app):
        self.app = app

    def display(self):
        ss = self.app.ss  # MyStSessionStateインスタンスを参照
        st.write(ss._df_sessions)
        df = ss.df
        cols_measure = ss.cols_measure
        ui_cols = st.columns(3)
        cols_key = [ col for col in list(df.columns) if col not in cols_measure ]
        with ui_cols[0]:
            ss.selected_rows = st.multiselect("Select Row Fields", cols_key , ss.selected_rows)
        with ui_cols[1]:
            ss.selected_cols = st.multiselect("Select Column Fields", cols_key, ss.selected_cols)

        with ui_cols[2]:
            ss.selected_value = st.selectbox(
                "Select Values Field", cols_measure
                , index=cols_measure.index(ss.selected_value) if ss.selected_value else 0)

