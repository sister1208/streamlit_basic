import numpy as np
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import json

st.title('Chart Elements')
st.header('1. Bar chart')
df = pd.DataFrame(np.random.rand(20,3), columns='A B C'.split())
st.dataframe(df)

st.bar_chart(df)
st.bar_chart(df['A'])
st.bar_chart(df, y='B')
st.bar_chart(df, x='C')

st.divider()
df2 = pd.DataFrame({'A':list(range(1,21)),
                    'B':np.random.rand(20),
                    'C':['x']*5+['y']*5+['z']*5+['w']*5})
st.dataframe(df2)
st.bar_chart(df2, x='A', y='B', color='C')
st.bar_chart(df2, x='A', y='B', color='#ff0000')
st.bar_chart(df2, x='A', y=['B','C'], color=['#ff0000', "#00ffea"])

st.divider()
st.header('2. Line Chart', divider=True)
st.line_chart(df)
st.line_chart(df['B'])

st.header('3. Area Chart', divider=True)
st.area_chart(df)
st.area_chart(df, y=['A','B'])
st.area_chart(df, y=['A','B'], stack=True)

st.header('4. Scatter plot', divider=True)
iris = pd.read_csv('data/iris.csv')
st.dataframe(iris)
st.scatter_chart(iris, x='sepal_length', y='petal_length')
st.scatter_chart(iris, x='petal_length', y='petal_width', color='species')
st.scatter_chart(iris, x='petal_length', y='petal_width',
                  color='species', size='sepal_length')


from numpy.random import default_rng as rng
st.header('5. Map', divider=True)

df = pd.DataFrame(
    rng(0).standard_normal((1000, 2)) / [50, 50] + [37.55, 127.04],
    columns=["lat", "lon"],
)

st.map(df)

st.write('서울시 구청 지도')
loc = {'강남구청':[37.52579, 127.0483],
        '서초구청':[37.49093, 127.0329],
        '동작구청':[37.51871, 126.9364],
        '구로구청':[37.50237, 126.8890],
        '양천구청' :[37.52007, 126.9549],
        '영등포구청': [37.54240, 126.8402],
        '관악구청': [37.48467, 126.9515],
        '용산구청' :[37.53804, 126.9913],
        '서대문구청': [37.58567, 126.9357],
        '마포구청' : [37.57003, 126.9019],
        '은평구청' : [37.60675, 126.9302],
        '종로구청' : [37.57615, 126.9790],
        '중구청' : [37.56798, 126.9975],
        '성북구청' : [37.59342, 127.0172],
        '동대문구청' : [37.57792, 127.0401],
        '중랑구청' : [37.60961, 127.0931],
        '노원구청' : [37.65664, 127.0559],
        '도봉구청' : [37.67214, 127.0462],
        '강북구청' : [37.64278, 127.0253],
        '광진구청' : [37.54104, 127.0826],
        '강동구청' : [37.53246, 127.1237],
        '송파구청' : [37.51803, 127.105]}

df_loc = pd.DataFrame(loc).T
df_loc.columns=['lat','lon']
st.write(df_loc)

st.map(df_loc, zoom=9, color='#00ff00')

st.header('6. folium을 이용한 Map 시각화', divider=True)
m = folium.Map(location=[37.57615, 126.9790], zoom_start=9)
mc = MarkerCluster().add_to(m)

for gu, pos in loc.items():
    folium.Marker(location=pos,
                  popup=folium.Popup(gu, max_width=100)).add_to(mc)

st_folium(m, width=400, height=300)

st.write('경기도 인구데이터 지도시각화(단계구분도)')

with open('data/경기도행정구역경계.json', encoding='utf-8') as f:
    geo = json.loads(f.read())
df_pop = pd.read_excel('data/경기도인구데이터.xlsx')
st.dataframe(df_pop)
# st.json(geo, expanded=3)
st.markdown('2007 경기도인구데이터')
m = folium.Map(location=[37.57615, 126.9790], zoom_start=8)
folium.GeoJson(geo).add_to(m)
folium.Choropleth(geo_data=geo,
                  data=df_pop,
                  columns=['구분', 2007],
                  key_on='feature.properties.name').add_to(m)
st_folium(m, width=600, height=400)