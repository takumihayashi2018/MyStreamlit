import streamlit as st
import pandas as pd
import numpy as np
import os
import pickle

class DataFrameApp:

    def __init__(self, df: pd.DataFrame):
        self._setup_initial_state(df)

    def _setup_initial_state(self, df: pd.DataFrame):
        if "df" not in st.session_state:
            st.session_state.df = df
        if "formulas" not in st.session_state:
            st.session_state.formulas = {}

    def display(self):
        self._column_operations_form()
        self._formula_check_form()
        self._output_form()
        self._load_form()
        st.write("DataFrame:")
        st.write(st.session_state.df)

    def _column_operations_form(self):
        with st.form(key='column_operations'):
            new_column_name = st.text_input("Enter new column name:")
            lambda_expression = st.text_input("Enter lambda expression (use 'x' for the dataframe and 'np' for numpy):", "x['A'] + np.sin(x['B'])")
            delete_column_name = st.selectbox("Choose a column to delete:", ["None"] + list(st.session_state.df.columns))
            submitted = st.form_submit_button("Apply Changes")

            if submitted:
                self._add_column(new_column_name, lambda_expression)
                self._delete_column(delete_column_name)

    def _add_column(self, new_column_name, lambda_expression):
        if new_column_name:
            try:
                st.session_state.df[new_column_name] = st.session_state.df.apply(lambda x: eval(lambda_expression, {"np": np, "x": x}), axis=1)
                st.session_state.formulas[new_column_name] = lambda_expression
                st.write(f"Added new column '{new_column_name}'")
            except Exception as e:
                st.write(f"Error: {e}")

    def _delete_column(self, delete_column_name):
        if delete_column_name != "None" and delete_column_name in st.session_state.df.columns:
            del st.session_state.df[delete_column_name]
            if delete_column_name in st.session_state.formulas:
                del st.session_state.formulas[delete_column_name]
            st.write(f"Deleted column '{delete_column_name}'")

    def _formula_check_form(self):
        with st.form(key='formula_check'):
            selected_column = st.selectbox("Choose a column to check its formula:", list(st.session_state.df.columns))
            submit_check = st.form_submit_button("Check Formula")
            
            if submit_check and selected_column in st.session_state.formulas:
                st.write(f"Formula for '{selected_column}': {st.session_state.formulas[selected_column]}")

    def _output_form(self):
        with st.form(key='output_form'):
            default_filename = "output_dataframe.pkl"
            filename = st.text_input("Specify the output filename:", default_filename)
            save_btn = st.form_submit_button("Save DataFrame as Pickle")

            if save_btn:
                self.output(filename)

    def output(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump((st.session_state.df, st.session_state.formulas), file)
            st.write(f"Data saved to {filename}")

    def _load_form(self):
        with st.form(key='load_form'):
            files = [f for f in os.listdir() if f.endswith('.pkl')]
            selected_file = st.selectbox("Select a file to load:", files)
            load_btn = st.form_submit_button("Load DataFrame from Pickle")

            if load_btn:
                self.load(selected_file)

    def load(self, filename):
        with open(filename, 'rb') as file:
            st.session_state.df, st.session_state.formulas = pickle.load(file)
            st.write(f"Data loaded from {filename}")

if __name__ == "__main__":
    initial_df = pd.DataFrame({
        'A': [1, 2, 3, 4],
        'B': [5, 6, 7, 8]
    })
    app = DataFrameApp(initial_df)
    app.display()

