# 데이터(Data) 요소들 

import streamlit as st
import numpy as np
import pandas as pd
import random

# 1. st.DataFrame()

# pandas의 데이터프레임 객체
df = pd.DataFrame(np.random.randn(50,20),
                  columns=[f'col {i}' for i in range(20)])
st.subheader('Pandas Dataframe')
st.write(df)
st.divider()

st.subheader('Streamlit st.dataframe()')
st.dataframe(df.style.highlight_max(axis=0))
st.divider()

df = pd.DataFrame(
    {
        "name": ["Roadmap", "Extras", "Issues"],
        "url": ["https://roadmap.streamlit.app", 
                "https://extras.streamlit.app",
                  "https://issues.streamlit.app"],
        "stars": [random.randint(0, 1000) for _ in range(3)],
        "views_history": [[random.randint(0, 5000) for _ in range(30)] for _ in range(3)],
    }
)
st.write(df)

st.dataframe(
    df,
    column_config={
        "name": "App name",
        "stars": st.column_config.NumberColumn(
            "Github Stars",
            help="Number of stars on GitHub",
            format="%d ⭐",
        ),
        "url": st.column_config.LinkColumn("App URL"),
        "views_history": st.column_config.LineChartColumn(
            "Views (past 30 days)", y_min=0, y_max=5000
        ),
    },
    hide_index=True,
)

st.divider()

df = pd.DataFrame({'first':[1,2,3,4,5],
                   'second':[10,20,30,40,50]})
st.checkbox('use container width', value=False,
             key='use_container_width')
st.dataframe(df,
             use_container_width=st.session_state.use_container_width)


# 2. st.data_editor()

df = pd.DataFrame(
    [{'command':'st.selectbox', 'rating':4, 'is_widget':True},
     {'command':'st.balloons', 'rating':5, 'is_widget':False},
     {'command':'st.time_input', 'rating':3, 'is_widget':True}
     ]
)

edited_df = st.data_editor(df, num_rows='dynamic')
favor_cmd = edited_df.loc[edited_df['rating'].idxmin()]['command']
st.markdown(f'가장 좋아하는 명령어 **{favor_cmd}**')
st.divider()

# 3. st.metric()

st.metric(label='Temperature', value='70 ℉', delta='-1.2 ℉')
st.metric(label='Temperature', value='25 ℃', delta='+1.2 ℃')


# 4. st.table()
st.markdown('엑셀파일 로딩 및 표시')
df = pd.read_excel('data/kor_news_260318-0319.xlsx')
st.dataframe(df)

st.markdown('st.table()')
out_table = st.table(df.iloc[:5])
