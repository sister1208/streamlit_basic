import streamlit as st
from datetime import datetime, date, time

st.header('Input Widgets')
st.subheader('1.Button', divider=True)
st.button('초기화', type='primary')
if st.button('안녕'):
    st.write('반가워 :smile:')
else:
    st.write('잘가 :raising_hand_woman:')

st.subheader('2. LinkButton & Page Link', divider=True)
st.link_button('google', 'https://www.google.com')

st.page_link(page='app.py', label='Home', icon='🏠')
st.page_link(page='pages/4_charts.py', label='Chart', icon='📊')
st.page_link(page='pages/2_data_elements.py', label='Data', icon='🤔')

st.subheader('3. Form Submit Button')
st.markdown('TeaxArea & TextInput')
with st.form(key='form1'):
    ids = st.text_input('ID')
    pw = st.text_input('Password', type='password')
    text = st.text_area('메모', placeholder='메모', max_chars=10)
    submit = st.form_submit_button('login')

if submit:
    st.write(f'id:{ids}, pw:{pw}')
    st.write(text)

st.divider()
# label_visibility 
#  -'visible' : label 텍스트를 정상적으로 화면에 표시
#               기본값
#  - 'hidden' : label 텍스트는 화면에 보이지 않지만
#               label 텍스트가 차지하는 공간은 유지
#  -'collapsed' : label을 표시하지 않고, 라벨이 차지하는 공간도 없앰
#               compact하게 보이게 할 때

st.write('label_visibility 인수 용도!')
st.text_input("이름(visible)",
              label_visibility="visible")
st.text_input("이름(hidden)",
              label_visibility="hidden")
st.text_input("이름(collapsed)",
              label_visibility="collapsed",
              placeholder="이름 입력")


st.subheader('4. Checkbox, Toggle & Radio')
agree = st.checkbox('찬성', value=False)
if agree:
    st.write('Good!')

on = st.toggle('select')
if on:
    st.write('Toggle On')
else:
    st.write('Toggle Off')

fruit = st.radio(label='좋아하는 과일은?',
                  options=['바나나','딸기','배'],
                  captions=['웃어요','달콤해요','시원해요'],
                  horizontal=True,  # 수평, 수직 여부
                  index=1)          # 0부터, 선택 순서
st.write(fruit)
if fruit=='바나나':
    st.write('바나나를 선택했군요!')
else:
    st.write('아쉽다~~~')

st.subheader('5. SelectBox')
fruit = st.selectbox(label='먹고 싶은 과일을 선택하세요!',
                      options=['수박','딸기','자몽'],
                      index=None, # 아무것도 선택되지 않은 상태 
                      placeholder='과일 선택!',
                      label_visibility='visible')
st.write(f'당신이 선택한 과일은 {fruit}')

st.subheader('6. MultiSelect')
fruits = st.multiselect('당신이 좋아하는 과일을 모두 선택하세요!',
               options=['수박','딸기','자몽',
                        '포도','감',
                        '망고','바나나'],
              default=None,
              placeholder='과일을 모두 선택해요')
st.write(f'당신이 선택한 과일은 {fruits}')

st.subheader('7. Select Slider')
first,last = st.select_slider('당신이 좋아하는 과일은?',
                 options=['수박','자몽',
                          '딸기','포도','감',
                          '망고','바나나'],
                 value=['딸기','망고'])
st.write(f'first:{first}, last:{last}')

first,last = st.select_slider('연도',
                 options=range(2020,2050,3),
                 value=[2026,2032])
st.write(f'fisrt:{first}, last:{last}')

st.subheader('8. Slider', divider=True)
# 정수 범위 반환 
score = st.slider('점수대', min_value=0,
          max_value=100, step=2,
          value=(50,75))
st.write(f'선택한 점수는 {score}')

st.subheader('9. Numeric Input elements')
# 숫자 선택&반환 (실수/정수)
# min_value, max_value, step 모두 같은 형식의 데이터형 지정해야 함
number = st.number_input('숫자 입력',
                min_value=10.0,
                max_value=50.0,
                step=0.5,format='%.1f')
st.write(f"선택한 숫자는 {number}")

st.subheader('10. Color picker')
color = st.color_picker('색상선택',
                         value='#00f900')
st.write(f'선택한 색상은 {color}')

from datetime import timedelta

st.subheader('11. Date / Time Input')
date = st.date_input('일자선택',
                     value=date(2025,12,31),
                     min_value=date(2025,12,1),
                     max_value=date(2026,3,31),
                     format='YYYY.MM.DD')
time = st.time_input('시간선택',
                     value=time(9,00),
                     step=timedelta(minutes=10))
st.write(f'{date}, {time}')