''' --- st_page_edit_module  ---'''
import streamlit as st
from .page import Page


class PageEditModule(Page):
    def __init__(self, app):
        self.app = app

    def display(self):
        ss = self.app.ss
        
        st.write("### Edit Custom Module Settings")

        # Default value from session state
        default_content = ss.module_content if 'module_content' in ss else ""

        # Text area for editing settings
        content = st.text_area("Module Settings", default_content)

        if st.button("Save"):
            ss.module_content = content
            st.success("Settings saved!")