''' --- st_page_generate_query  ---'''
import streamlit as st

class PageGenerateQuery(Page):
    def generate_query(self):
        return query
    
    def display(self):
        st.write("### Generate Query")
        ss.query = self.generate_query()
        if query:
            st.code(ss.query, language="sql")
