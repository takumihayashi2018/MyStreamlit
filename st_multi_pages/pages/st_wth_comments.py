import streamlit as st
import pandas as pd

class CommentableDataFrame:
    def __init__(self, df: pd.DataFrame, comment_column_name='Comments'):
        self.comment_column_name = comment_column_name
        if self.comment_column_name not in df.columns:
            df[self.comment_column_name] = ["" for _ in range(len(df))]
        self.df = df

    def display(self):
        # Column headers
        cols = st.columns(len(self.df.columns) + 1)  # Add one more column for the action button
        fields = list(self.df.columns) + ['Action']

        for col, field in zip(cols, fields):
            col.write("**"+field+"**")

        for idx, row in self.df.iterrows():
            row_cols = st.columns(len(self.df.columns) + 1)
            
            for col, value in zip(row_cols[:-1], row):
                col.write(value)
            
            action_col = row_cols[-1]
            placeholder = action_col.empty()
            show_more = placeholder.button("more", key=str(idx))

            if show_more:
                placeholder.button("less", key=str(idx) + "_")
                
                # Display comment input and save button for the row
                with st.form(key=f'form_{idx}'):
                    user_comment = st.text_input("コメントを入力してください", value=row[self.comment_column_name])
                    submitted = st.form_submit_button("保存")
                    
                    if submitted:
                        self.df.at[idx, self.comment_column_name] = user_comment
                        st.success(f"Row {idx} のコメントが保存されました！")

# 使用例
data = {
    "ID": [1, 2, 3],
    "Name": ["Alice", "Bob", "Charlie"]
}

df = pd.DataFrame(data)
commentable_df = CommentableDataFrame(df, comment_column_name='Feedback')
commentable_df.display()


with st.form(key = "sample"):
    st.multiselect("dir0", ["banana","apple","chocolat"])
    st.form_submit_button("Data load")
