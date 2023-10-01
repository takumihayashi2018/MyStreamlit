# -*- coding: utf-8 -*-

import os
from MyModules.PyDesktop.my_doc_diff import MyDocDiff
import streamlit as st
from io import StringIO

from pages.custom_module2.st_main import MyStSessionState

def file_loader(label="Choose a file"):
    uploaded_file = st.file_uploader(label)
    
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        content = stringio.getvalue()
        #st.write(content)
        return content

class DocDiffApp:
    def __init__(self):
        self.ss = MyStSessionState(doc1=None, doc2=None)
        
    def display(self):
        st.write("#### DocDiffApp")
        ss = self.ss        
        ss.doc1 = file_loader(label="Choose the first file")
        ss.doc2 = file_loader(label="Choose the second file")
        
        if ss.doc1 and ss.doc2:  # Check if both documents are uploaded
            dd = MyDocDiff()
            dd.compare(ss.doc1, ss.doc2)
            diff_html = '<meta charset="UTF-8">' + dd.str_html
            st.markdown(diff_html, unsafe_allow_html=True)
            with open("output.html", "w") as file:
                file.write(diff_html) 

            # HTMLファイルを読み込む
            # with open("output5.html", 'r') as file:
            with open("output_diff2.html", 'r') as file:
                html_content = file.read()
            st.markdown(html_content, unsafe_allow_html=True)

    
            

if __name__ == "__main__":
    app = DocDiffApp()
    app.display()

