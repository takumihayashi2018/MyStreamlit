''' --- st_page_data_frame_display  ---'''
import pandas as pd
import streamlit as st
import numpy as np
from .page import Page


class PageDataFrameDisplay(Page):
    """データフレーム表示画面を表示するページ"""
    def __init__(self, app):
        self.app = app
    
    def display(self):
        ss = self.app.ss  # MyStSessionStateインスタンスを参照
        self.show_selected_params(ss)
        
        # ss.selected_colsが空の場合
        if not ss.selected_cols and not ss.selected_rows:
            st.write(ss.df)
            return
            
        if not ss.selected_cols:
            ss.grouped_df = ss.df.groupby(ss.selected_rows).agg({ss.selected_value: np.sum}).reset_index()
            
            st.write(ss.grouped_df)
            return

        if ss.selected_rows and ss.selected_cols and ss.selected_value:
            pivot_table = pd.pivot_table(
                ss.df
                , values = ss.selected_value
                , index = ss.selected_rows
                , columns = ss.selected_cols
                , aggfunc = np.sum
            )

            if pivot_table.columns.nlevels > 1:
                pivot_table.columns = ['_'.join(map(str, col)) for col in pivot_table.columns.values]

            st.write(pivot_table)
        else:
            st.write(
                "Please select both Row and Column fields" \
                + " and a Value field to generate Pivot Table."
            )
            
        self.show_comment_box()
        
    def show_selected_params(self, ss):
        st.write("Selected Rows:", ", ".join(ss.selected_rows))
        st.write("Selected Columns:"
                 , ", ".join(ss.selected_cols) if ss.selected_cols else "None")
        st.write("Selected Value:", ss.selected_value)

    def show_comment_box(self):
         # コメントボックス
        user_comment = st.text_area("Leave your comment here:")
        if user_comment:
            st.write("Your Comment:", user_comment)
