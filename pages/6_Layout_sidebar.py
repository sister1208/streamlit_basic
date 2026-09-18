import streamlit as st

with st.sidebar:
    result = st.radio('학년',
                      options=['1학년',
                               '2학년',
                               '3학년'])
    st.write(f'학년은? :{result}')

color = st.sidebar.selectbox('색상', ['Red','Blue'])
st.write(color)

with st.sidebar:
    st.page_link('pages/1_text_elements.py',
                 label='Text')
    st.page_link('https://www.naver.com',
                 label='Naver')
    