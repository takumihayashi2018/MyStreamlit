import streamlit as st
import pandas as pd

class MyStSessionState:
    def __init__(self, **initial_values):
        # _df_sessions を初期化
        self._df_sessions = pd.DataFrame(columns=["property_name", "initial_value", "value"])
        for name, value in initial_values.items():
            if name not in self:
                self.__setattr__(name, value)
                self._update_df_sessions(name, value, value)

    def refresh(self, ls_property_names):
        """指定されたプロパティを初期値にリセットする"""
        df = self._df_sessions
        for name in ls_property_names:            
            if name in df['property_name'].values:
                idx = df[df['property_name'] == name].index[0]
                initial_value = df.at[idx, 'initial_value']
                self.__setattr__(name, initial_value)

    def _update_df_sessions(self, name, initial_value, value):
        # _df_sessions を更新するための内部メソッド
        new_row = pd.DataFrame([{
            "property_name": name,
            "initial_value": initial_value,
            "value": value
        }])
        
        self._df_sessions = pd.concat([self._df_sessions, new_row], ignore_index=True)


    def __getattr__(self, name):
        if name == "_df_sessions":
            return st.session_state[name] if name in st.session_state else None
        return st.session_state[name] if name in st.session_state else None

    def __setattr__(self, name, value):
        if name == "_df_sessions":
            st.session_state[name] = value
        elif name != "initialized" and not name.startswith('_'):
            st.session_state[name] = value
            if name not in self._df_sessions['property_name'].values:
                self._update_df_sessions(name, value, value)
            else:
                idx = self._df_sessions[self._df_sessions['property_name'] == name].index[0]
                self._df_sessions.at[idx, 'value'] = value
        else:
            super().__setattr__(name, value)

    def __contains__(self, key):
        return key in st.session_state

