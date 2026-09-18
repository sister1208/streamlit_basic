import streamlit as st

from config import ANALYSIS_COLUMNS
from db.order_crud import get_sales_analysis


def render_analysis_view():
    st.subheader("📊 매출 분석")
    group_label = st.segmented_control(
        "분석 기준", list(ANALYSIS_COLUMNS), default="카테고리"
    )
    top_n = st.slider("상위 항목 개수", 3, 10, 5)
    include_discount = st.checkbox("할인 금액 반영", value=True)

    summary = get_sales_analysis(group_label, top_n, include_discount)
    if summary.empty:
        st.info("분석할 주문 데이터가 없습니다.")
        return

    display = summary.rename(columns={
        "analysis_group": group_label,
        "sales_amount": "매출액",
    })
    st.bar_chart(display, x=group_label, y="매출액")
    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "매출액": st.column_config.NumberColumn("매출액", format="₩ %d")
        },
    )
