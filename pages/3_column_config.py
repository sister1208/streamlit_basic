import numpy as np
import pandas as pd
from datetime import datetime, date, time
import streamlit as st

st.header('Data Column Config', divider=True)
df = pd.DataFrame(
    {
        "category": [
            "📊 Data Exploration",
            "📈 Data Visualization",
            "🤖 LLM",
            "📊 Data Exploration",
        ],
    }
)
st.data_editor(df)

st.divider()

st.markdown('Column_config : SelectboxColumn')
col_config1 = {'category': st.column_config.SelectboxColumn('App Category',
                                                            help='The category of the app',
                                                            width='medium',
                                                            options=["📊 Data Exploration",
                                                                     "📈 Data Visualization",
                                                                     "🤖 LLM",],
                                                            required=True)}
st.data_editor(df, column_config=col_config1, hide_index=True)

st.markdown('Column_config: DatetimeColumn')
df = pd.DataFrame({
    'meeting_time':[datetime(2025,2,5,12,30), 
                    datetime(2025,2,7,2,30), 
                    datetime(2025,4,5,10,00)],
    'site' :['Naver', 'Daum', 'Google'],
    'url':['https://www.naver.com',
           'https://www.daum.net',
           'https://www.google.com']
})

st.data_editor(df)
            

col_config2 = {
    'meeting_time': st.column_config.DatetimeColumn(min_value=datetime(2026,1,1),
                                                    max_value=datetime(2026,3,31),
                                                    format='D MMM YYYY, h:mm a'),
    'url' : st.column_config.LinkColumn(max_chars=100,
                                        validate=r'^https?://www\.[a-z]+\.[a-z]+',
                                        display_text='Search site')}

st.data_editor(df, column_config=col_config2, hide_index=True)