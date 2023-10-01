import streamlit as st
import pandas as pd

class MyStSessionState:
    def __init__(self, **initial_values):
        # _df_sessions を初期化
        if '_df_sessions' not in st.session_state:
            st.session_state['_df_sessions'] = pd.DataFrame(columns=["property_name", "initial_value", "value"])
        
        for name, value in initial_values.items():
            self.__setattr__(name, value)
            self._update_df_sessions(name, value, value)

    def _update_df_sessions(self, name, initial_value, value):
        # _df_sessions を更新するための内部メソッド
        st.session_state['_df_sessions'] = st.session_state['_df_sessions'].append({
            "property_name": name,
            "initial_value": initial_value,
            "value": value
        }, ignore_index=True)

    def __getattr__(self, name):
        return st.session_state[name] if name in st.session_state else None

    def __setattr__(self, name, value):
        if name != "initialized" and not name.startswith('_'):
            st.session_state[name] = value
            if name not in st.session_state['_df_sessions']['property_name'].values:
                self._update_df_sessions(name, value, value)
            else:
                idx = st.session_state['_df_sessions'][st.session_state['_df_sessions']['property_name'] == name].index[0]
                st.session_state['_df_sessions'].at[idx, 'value'] = value
        else:
            super().__setattr__(name, value)

    def __contains__(self, key):
        return key in st.session_state

    def refresh(self, ls_property_names):
        """指定されたプロパティを初期値にリセットする"""
        for name in ls_property_names:
            if name in st.session_state['_df_sessions']['property_name'].values:
                idx = st.session_state['_df_sessions'][st.session_state['_df_sessions']['property_name'] == name].index[0]
                initial_value = st.session_state['_df_sessions'].at[idx, 'initial_value']
                self.__setattr__(name, initial_value)

# 使用例
state = MyStSessionState(my_prop="initial_value", another_prop="initial_value_2")

# プロパティの状態を更新
state.my_prop = "new_value"
state.another_prop = "new_value_2"

# 更新後のプロパティの状態を表示
st.write(st.session_state['_df_sessions'])

# my_propとanother_propを初期化
state.refresh(['my_prop', 'another_prop'])

# 初期化後のプロパティの状態を表示
st.write(st.session_state['_df_sessions'])
