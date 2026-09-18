import streamlit as st
import numpy as np
import time

st.title('Container')
# container :  화면에 요소(elements)를 담아두는 레이아웃/출력영역 객체
# st.write()처럼 즉시 출력
# st.container()를 쓰면 출력 위치를 미리 확보해두고 그 안에 여러 요소들을 넣거나
#       갱신할 수 있게 함
# 대표적인 컨테이너
# - st.container() st.sidebar()
# - st.columns()   st.expander()
# - st.tabs(), st.empty(), st.popover()

st.header('1. Column Layout')
imgs = ['https://static.streamlit.io/examples/cat.jpg',
        'https://static.streamlit.io/examples/dog.jpg',
        'https://static.streamlit.io/examples/owl.jpg']
# 아래 코드와 동일
# cols = st.columns(3)
# # st.write(len(cols))
# for i in range(3):
#     cols[i].subheader(f'Col{i+1}')
#     cols[i].image(imgs[i])

col1, col2, col3 = st.columns(3,
                              gap='large',
                              vertical_alignment='top') # 세로방향의 정렬 방식 
col1.subheader('Col1')
col1.image(imgs[0])
col2.subheader('Col2')
col2.image(imgs[1])
col3.subheader('Col3')
col3.image(imgs[2])

st.divider()
col1, col2, col3 = st.columns([1,2,2], # 비율로도 설정 가능 
                              gap='medium',
                              vertical_alignment='center')
data = np.random.rand(10,1)
with col1:
    st.metric('점수', 55, 0.5)
with col2:
    st.line_chart(data)
with col3:
    st.bar_chart(data)
# col1.metric()와 같은 표현

st.divider()
st.header('2. Container')
with st.container(border=True): # border : 외곽선 
    st.write('컨테이너 내부')
    st.bar_chart(np.random.randn(50))

st.write('컨테이너 외부')
cont = st.container(border=True)
cont.write('컨테이너 내부')
cont.area_chart(np.random.randn(50))
cont.button('버튼')
st.write('컨테이너 외부')

st.divider()
st.subheader('1) 그리드 모양의 컨테이너 구성')
row1 = st.columns(3)
row2 = st.columns(2)
for col in row1+row2: # 컨테이너 총 5개
    tile = col.container(height=100)
    tile.markdown(':smile:')

st.subheader('2) scollbar가 있는 컨테이너')
with st.container(height=300):
    st.markdown('long_text '*300)

st.divider()
st.header('3. Empty Container : Single element')
# empty() : 나중에 내용을 넣거나, 덮어쓰거나, 비울 수 있는
#     1칸짜리 placeholder와 같은 역할을 함
# 메모리 효율화를 위해 사용
with st.empty():
    for sec in range(10):
        st.write(f'{sec}초')
        time.sleep(1)
    st.write('time over')

# for i in range(10):
#     st.write(f'현재 진행률 {i+1}/10')
#     time.sleep(1)
# 메시지 5개 생성, html DOM 요소 증가, 랜더링 부담증가

place = st.empty()
for i in range(10):
    place.write(f'현재 진행률 {i+1}/10')
    time.sleep(0.5)