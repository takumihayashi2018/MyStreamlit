import streamlit as st

class MyStSessionState:
    def __getattr__(self, name):
        # このメソッドは、指定された属性の値を取得するときに呼ばれます
        # st.session_stateから値を取得します
        return st.session_state[name] if name in st.session_state else None

    def __setattr__(self, name, value):
        # このメソッドは、指定された属性に値をセットするときに呼ばれます
        # st.session_stateに値をセットします
        if name != "initialized" and not name.startswith('_'):
            st.session_state[name] = value
        else:
            super().__setattr__(name, value)

    def __contains__(self, key):
        # 特定のキーがst.session_stateに存在するかを確認するためのメソッド
        return key in st.session_state
