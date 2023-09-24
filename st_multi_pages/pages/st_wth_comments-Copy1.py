import streamlit as st
import pandas as pd

class CommentableDataFrame:
    def __init__(self, df: pd.DataFrame, comment_column_name='Comments'):
        self.comment_column_name = comment_column_name
        if self.comment_column_name not in df.columns:
            df[self.comment_column_name] = ["" for _ in range(len(df))]
        self.df = df
        self.selected_id = None

    def display(self):
        for index, row in self.df.iterrows():
            btn_label = f"詳細 - {row['ID']} - {row['Name']}"
            if st.button(btn_label):
                self.selected_id = row['ID']

        if self.selected_id is not None:
            selected_row = self.df[self.df["ID"] == self.selected_id]
            st.write(selected_row)

            with st.form(key='comment_form'):
                user_comment = st.text_input("コメントを入力してください", value=selected_row[self.comment_column_name].iloc[0])
                
                # フォーム内に送信ボタンを配置
                submitted = st.form_submit_button("コメントを保存")

                if submitted:
                    self.df.loc[self.df["ID"] == self.selected_id, self.comment_column_name] = user_comment
                    st.success("コメントが保存されました！")

        st.table(self.df)

# 使用例
data = {
    "ID": [1, 2, 3],
    "Name": ["Alice", "Bob", "Charlie"]
}
df = pd.DataFrame(data)
commentable_df = CommentableDataFrame(df, comment_column_name='Feedback')
commentable_df.display()
