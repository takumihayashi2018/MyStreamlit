import os
import pandas as pd
import streamlit as st
from .page import Page

class PageSave(Page):
    """設定したパラメータを保存するページ"""
    def __init__(self, app):
        self.app = app

    def display(self):
        ss = self.app.ss
        save_path = st.text_input("Specify the save path:")
        if save_path:
            if os.path.exists(os.path.dirname(save_path)) \
                or os.path.dirname(save_path) == '':
                ss.df.to_csv(save_path, index=False)
                st.success(f"Saved to {save_path}")
            else:
                st.error("The specified directory does not exist.")
