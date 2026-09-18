from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(
    page_title="드론 입찰공고 대시보드",
    page_icon="🚁",
    layout="wide"
)

st.title("🚁 대한민국 공공 분야 드론 입찰공고 분석 대시보드")
st.caption("2020년 ~ 2026년 나라장터 입찰공고 내역 통합 데이터")

# 2. 데이터 로드 및 전처리 (캐싱 처리)
@st.cache_data
def load_data():
    # test.py(pages 폴더) 기준 상위 폴더(Streamlit_Basic)의 CSV 파일 경로 지정
    base_dir = Path(__file__).resolve().parent.parent
    csv_path = base_dir / "입찰공고내역_통합.csv"

    if not csv_path.exists():
        st.error(f"파일을 찾을 수 없습니다: {csv_path}")
        st.stop()

    df = pd.read_csv(csv_path)

    # 공고일자 날짜형 변환
    df["공고일자_dt"] = pd.to_datetime(
        df["공고일자"].astype(str), format="%Y%m%d", errors="coerce"
    )
    df["연도"] = df["공고일자_dt"].dt.year
    df["월"] = df["공고일자_dt"].dt.month

    # 숫자 데이터 콤마 제거 및 형변환
    num_cols = ["배정예산", "추정가격", "기초금액", "입찰자수"]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", ""), errors="coerce"
            ).fillna(0)

    return df

df_raw = load_data()

# ----------------------------------------------------
# 3. 사이드바 필터
# ----------------------------------------------------
st.sidebar.header("🔍 검색 및 필터")

# 연도 필터
years = sorted([int(y) for y in df_raw['연도'].dropna().unique()])
selected_years = st.sidebar.multiselect("연도 선택", years, default=years)

# 업무구분 필터
categories = sorted(df_raw['업무구분'].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect("업무 구분", categories, default=categories)

# 계약방법 필터
contract_methods = sorted(df_raw['계약방법'].dropna().unique().tolist())
selected_contracts = st.sidebar.multiselect("계약 방법", contract_methods, default=contract_methods)

# 공고명 검색어
search_keyword = st.sidebar.text_input("공고명 검색어", "")

# 데이터 필터링 적용
filtered_df = df_raw[
    (df_raw['연도'].isin(selected_years)) &
    (df_raw['업무구분'].isin(selected_categories)) &
    (df_raw['계약방법'].isin(selected_contracts))
]

if search_keyword:
    filtered_df = filtered_df[filtered_df['공고명'].astype(str).str.contains(search_keyword, case=False, na=False)]

# ----------------------------------------------------
# 4. 메인 대시보드 - KPI 카드
# ----------------------------------------------------
m1, m2, m3, m4 = st.columns(4)

total_bids = len(filtered_df)
total_budget = filtered_df['배정예산'].sum() / 100_000_000  # 억 원 단위
avg_bidders = filtered_df['입찰자수'].mean()
total_agencies = filtered_df['수요기관'].nunique()

m1.metric("총 공고 건수", f"{total_bids:,} 건")
m2.metric("총 배정예산 규모", f"{total_budget:,.1f} 억 원")
m3.metric("평균 경쟁률", f"{avg_bidders:.1f} 명/건")
m4.metric("발주 수요기관 수", f"{total_agencies:,} 개")

st.markdown("---")

# ----------------------------------------------------
# 5. 시각화 차트 (Plotly)
# ----------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 연도별 공고 건수 및 예산 추이")
    yearly_summary = filtered_df.groupby('연도').agg(
        공고건수=('입찰공고번호', 'count'),
        총예산_억원=('배정예산', lambda x: x.sum() / 100_000_000)
    ).reset_index()
    
    fig_year = px.bar(
        yearly_summary, x='연도', y='공고건수',
        text='공고건수',
        title="연도별 발주 건수",
        labels={'공고건수': '공고 건수', '연도': '연도'},
        color_discrete_sequence=['#1f77b4']
    )
    st.plotly_chart(fig_year, use_container_width=True)

with col2:
    st.subheader("🏛️ 최다 발주 수요기관 TOP 10")
    top_agencies = filtered_df['수요기관'].value_counts().head(10).reset_index()
    top_agencies.columns = ['수요기관', '공고건수']
    
    fig_agency = px.bar(
        top_agencies, y='수요기관', x='공고건수',
        orientation='h',
        text='공고건수',
        title="상위 10개 발주 기관",
        color='공고건수',
        color_continuous_scale='Blues'
    )
    fig_agency.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_agency, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("🧩 업무구분별 비중")
    cat_summary = filtered_df['업무구분'].value_counts().reset_index()
    cat_summary.columns = ['업무구분', '건수']
    
    fig_pie = px.pie(
        cat_summary, names='업무구분', values='건수',
        hole=0.4,
        title="업무구분 분포"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col4:
    st.subheader("📑 계약방법별 분포")
    contract_summary = filtered_df['계약방법'].value_counts().head(7).reset_index()
    contract_summary.columns = ['계약방법', '건수']
    
    fig_contract = px.bar(
        contract_summary, x='계약방법', y='건수',
        text='건수',
        color='계약방법'
    )
    st.plotly_chart(fig_contract, use_container_width=True)

# ----------------------------------------------------
# 6. 세부 데이터 테이블 및 다운로드
# ----------------------------------------------------
st.markdown("---")
st.subheader("📋 세부 공고 내역 목록")

# 주요 컬럼만 선별하여 출력
display_cols = ['공고일자', '입찰공고번호', '공고명', '수요기관', '업무구분', '계약방법', '배정예산', '입찰자수']
available_cols = [c for c in display_cols if c in filtered_df.columns]

st.dataframe(filtered_df[available_cols], use_container_width=True)

# CSV 다운로드 버튼
csv_data = filtered_df.to_csv(index=False, encoding='utf-8-sig')
st.download_button(
    label="📥 필터링된 데이터 CSV 다운로드",
    data=csv_data,
    file_name="드론_입찰공고_검색결과.csv",
    mime="text/csv"
)