import streamlit as st
from .page import Page
from .st_page_load import PageLoad


class PagePagesLoad(Page):
    """データフレーム表示画面を表示するページ"""
    def __init__(self, app):
        self.app = app
        self.pages = {
            "Load Data1": PageLoad(app),
            "Load Data2": PageLoad(app),          
        }

    def display(self):
        ss = self.app.ss
        st.write("#### Load Files")
        
        # ラジオボタンでページを選択
        page_name = st.radio("Choose a page:", list(self.pages.keys()))

        # 選択されたページを表示
        page = self.pages[page_name]
        page.display()
