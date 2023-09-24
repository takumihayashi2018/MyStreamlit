import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

query = '''
'''

st.title("Credit XXX Summary")


with st.form(key = "creditXXX"):
    st.multiselect("dir0", ["banana","apple","chocolat"])
    st.form_submit_button("Data load")
    

