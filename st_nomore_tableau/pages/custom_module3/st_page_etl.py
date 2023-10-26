import streamlit as st
from .page import Page

class PageEtl(Page):
    """カラム選択画面を表示するページ"""
    def __init__(self, app):
        self.app = app
        

    def choose_df(self):
        ss = self.app.ss
        
        if ss.ls_load_keys:
            ss.selected_load_key = st.selectbox("Select load key:", ss.ls_load_keys)
        else:
            ss.selected_load_key = None
        st.write(f"{ss.selected_load_key} is selected.")

    def merge_dfs(self):
        if len(dataframes) > 1:
            merge_option = st.selectbox("マージタイプを選択してください", ["内部結合", "外部結合", "左結合", "右結合"])
            on_col = st.text_input("どの列でマージしますか？ (カンマ区切りで複数指定可能)")
        
            # マージ操作の実行
            if st.button("マージ"):
                cols = on_col.split(',')
                if merge_option == "内部結合":
                    merged_df = pd.merge(dataframes[0], dataframes[1], on=cols, how='inner')
                elif merge_option == "外部結合":
                    merged_df = pd.merge(dataframes[0], dataframes[1], on=cols, how='outer')
                elif merge_option == "左結合":
                    merged_df = pd.merge(dataframes[0], dataframes[1], on=cols, how='left')
                elif merge_option == "右結合":
                    merged_df = pd.merge(dataframes[0], dataframes[1], on=cols, how='right')
                
                st.write(merged_df)

    def display(self):
        st.write("Page for ETL")
        st.write(
        '''
        WIP  
        You can do the followings:  
        - merge some data frames
        - add / delete columns with formulas
        - check formulas
        '''
        )
        self.choose_df()
