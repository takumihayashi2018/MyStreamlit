import streamlit as st
from .page import Page
from .st_page_load import PageLoad


class PagePagesLoad(Page):
    """データフレーム表示画面を表示するページ"""
    def __init__(self, app):
        self.app = app
        ss = self.app.ss

        self.pages = {
            "Load Data1": PageLoad(app, 'load1'),
            "Load Data2": PageLoad(app, 'load2'),          
        }

    def display(self):
        ss = self.app.ss
        st.write("#### Load Files")
        st.write(
        '''
        WIP  
        You will be able to load data frames:  
        - from denodo
          - with sql queries, or
          - with some inputs with simple UI
        - from csv
        - from pickle ( i.e. saved data via this app )
        '''
        )
        
        # ラジオボタンでページを選択
        page_name = st.radio("Choose a page:", list(self.pages.keys()))

        # 選択されたページを表示
        page = self.pages[page_name]
        page.display()
