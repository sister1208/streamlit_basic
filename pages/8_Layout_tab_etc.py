import streamlit as st

st.header('1. Tab')

label_seq = ['Cat', 'Dog','Owl']
img_seq = ['https://static.streamlit.io/examples/cat.jpg',
           'https://static.streamlit.io/examples/dog.jpg',
           'https://static.streamlit.io/examples/owl.jpg']
# tab_seq = st.tabs(label_seq)

# for i, label in enumerate(label_seq):
#     tab_seq[i].markdown(label_seq[i])
#     tab_seq[i].image(img_seq[i], width=200)

tab1, tab2, tab3 = st.tabs(label_seq)
with tab1:
    tab1.markdown(label_seq[0])
    tab1.image(img_seq[0], width=200)
with tab2:
    tab2.markdown(label_seq[1])
    tab2.image(img_seq[1], width=200)
with tab3:
    tab3.markdown(label_seq[2])
    tab3.image(img_seq[2], width=200)

st.divider()

st.header('2. Expander')

with st.expander('설명', expanded=False):
    st.markdown('''
다음은 expander에 대한 사용 형식과 기능을 설명한 내용입니다.<br>
st.expander(label, ...)
             ''')
    st.image('img/apple.png')

expd = st.expander('expander 사용시 주의점', expanded=True)
expd.write('expander 내에 다른 expander 객체를 둘 수 없음!')

st.header('3. PopOver')
with st.popover('Open popover'):
    st.write('Hello PopOver!')
    name = st.text_input('이름은? ')
st.write(f'이름 : {name}')

popov = st.popover('선호 색상은:', 
                   use_container_width=True)
red = popov.checkbox('red', True)
blue = popov.checkbox('blue')
if red:
    st.write(':red[빨강]')
if blue:
    st.write(':blue[파랑]')

with st.popover('popover 사용시 주의점'):
    st.write('popover내에 다른 popover 배치 불가!')
