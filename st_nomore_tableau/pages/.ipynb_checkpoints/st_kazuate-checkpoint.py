import streamlit as st
import random
from pages.custom_module.my_st_session_state import MyStSessionState

ss = MyStSessionState()

if 'secret_number' not in ss:
    ss.secret_number = random.randint(1, 100)
    ss.attempts = 0

st.title('数当てゲーム')

guess = st.number_input('1から100までの数を当ててみてください', min_value=1, max_value=100)
if st.button('確認'):
    ss.attempts += 1
    if guess == ss.secret_number:
        st.success(f'正解！ {ss.attempts}回で当てました！')
        ss.secret_number = random.randint(1, 100)  # 新しい数を生成
        ss.attempts = 0
    elif guess < ss.secret_number:
        st.warning('もっと大きい数です！')
    else:
        st.warning('もっと小さい数です！')

