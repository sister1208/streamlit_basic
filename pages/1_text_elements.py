# 화면 출력 요소들

import streamlit as st

# 텍스트 요소들(headings and body texts)

#1. Title : st.title(body, anchor=None, ...)
st.title('텍스트 요소들: This is title!')

#2. Header : st.header(body, anchor=Noen, ..., divider=False, ...)
st.header('국방장비 운용현황', divider=True)

#3. Subheader : st.subheader(body, anchor=Noen, ..., divider=False, ...)
st.subheader('1. 전차', divider='rainbow')

#4. Caption : st.caption(body, unsafe_allow_html=False, *, help=None, 
#                        width="stretch", text_alignment="left")
st.caption('데이터 기준일: 2026-09-14')

#5. Code block : st.code(body, language='', line_number=False, ...)
code = '''
def hello():
    print('hello streamlit: code block')
'''
st.code(code, language='python', line_numbers=True)

#6. Markdown : st.markdown(body, unsafe_allow_html=False, *, 
#                           help=None, width="auto", text_alignment="left")
st.markdown('*Streamlit* is **really** ***cool***')
st.markdown('''
    :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
    :gray[pretty] :rainbow[colors] and :blue-background[highlight] text.''')
st.markdown("Here's a bouquet &mdash;\
            :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")

# 7. Preformatted text: st.text(body)
st.text('This is some text!!!')

multi = '''If you end a line with two spaces,
a soft return is used for the next line.

Two (or more) newline characters in a row will result in a hard return.
'''
# 8. Horizonal rule: st.divider()
st.text(multi)
st.divider()
st.markdown(multi)

st.divider()

st.subheader('st.writer()')
# 9. 쓰기 : st.write()
# 1) 텍스트 쓰기
st.write('Hello, *Streamlit!* :banana:')

def get_user_name():
    return 'Acorn'

def get_greeting():
    return 'Hello'

punc = '!'
st.write(get_greeting(), punc, get_user_name())
st.divider()


# 2) 데이터프레임 객체 쓰기
import pandas as pd
st.write('Sample Dataframe')
df = pd.DataFrame({'first':[1,2,3,4,5],
                   'second':[100,200,300,400,500]})
st.write(df)
st.divider()

# 3) Chart객체 쓰기 
import numpy as np
import altair as alt

df = pd.DataFrame(np.random.randn(200,3),
                   columns='A B C'.split())
chart = alt.Chart(df).mark_circle().encode(x='A', y='B',
                                           size='C',
                                           color='C',
                                   tooltip=['A','B','C'])
st.write(chart)
st.divider()

# 10. 수식 : st.latex()
st.subheader('수식 latex()')
st.latex(r'b \over a')
st.latex(r'\sqrt {x^2 + y^2}')

# 11. echo()  :st.echo()
with st.echo():
    def get_punc():
        return '!!!!'

    greeting='Hi'
    value = get_user_name()
    punc = get_punc()
    st.write(greeting, value, punc)


# 12. st.balloons(), st.snow()
st.balloons()
st.snow()
st.spinner()
 # st.error()