import pandas as pd
import streamlit as st

ss = st.session_state

class MyStSessionState:
    def __init__(self, **initial_values):
        if '_df_init' not in ss:
            ss['_df_init'] = pd.DataFrame(
                columns=["property_name", "initial_value"]
            )
        
        for name, value in initial_values.items():
            if name not in ss:
                self.update_df_init(name, value)
                self.__setattr__(name, value)

    def update_df_init(self, name, value):
        if name not in ss:
            new_record = pd.DataFrame({
                "property_name" : [name]
                , "initial_value" : [value]
            })
                
            ss['_df_init'] = pd.concat(
                [ss._df_init, new_record], axis = 0
            )
        
    def __getattr__(self, name):
        return ss[name] if name in ss else None

    def __setattr__(self, name, value):
        # このメソッドは、指定された属性に値をセットするときに呼ばれます
        # ssに値をセットします
        if not name.startswith('_'):
            ss[name] = value
        else:
            self.update_df_init(name, value)
            super().__setattr__(name, value)

    def __contains__(self, key):
        # 特定のキーがssに存在するかを確認するためのメソッド
        return key in ss
        
    @property
    def _df(self):
        __df = self._df_init.copy()
        __df["value"] = __df.apply(lambda x: f"{ss[x.property_name]}", axis = 1)
        return __df

    def refresh(self, ls_property_names):
        df_init = ss['_df_init']
        
        for name in ls_property_names:
            if name in df_init['property_name'].values:
                initial_value = df_init.set_index("property_name").at[name, "initial_value"]
                self.__setattr__(name, initial_value)
        
    
