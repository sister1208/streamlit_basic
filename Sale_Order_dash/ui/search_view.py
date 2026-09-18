import streamlit as st

from config import CATEGORIES, ORDER_STATUSES, REGIONS
from db.order_crud import get_order_summary, search_orders


def _current_filters():
    return {
        "keyword": st.session_state.search_keyword,
        "categories": st.session_state.search_categories,
        "regions": st.session_state.search_regions,
        "status": st.session_state.search_status,
        "start_date": st.session_state.search_start_date,
        "end_date": st.session_state.search_end_date,
        "urgent_only": st.session_state.search_urgent_only,
    }


def render_search_view():
    st.subheader("🔍 주문 검색")
    with st.form("search_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            keyword = st.text_input("고객명 또는 상품명", st.session_state.search_keyword)
            categories = st.multiselect("카테고리", CATEGORIES, st.session_state.search_categories)
        with col2:
            regions = st.multiselect("지역", REGIONS, st.session_state.search_regions)
            status_options = ["전체"] + ORDER_STATUSES
            status = st.selectbox(
                "처리 상태", status_options,
                index=status_options.index(st.session_state.search_status),
            )
        with col3:
            period = st.date_input(
                "주문 기간",
                value=(st.session_state.search_start_date, st.session_state.search_end_date),
            )
            urgent_only = st.toggle("긴급 주문만 조회", st.session_state.search_urgent_only)
        submitted = st.form_submit_button("검색", type="primary", use_container_width=True)

    if submitted:
        st.session_state.search_keyword = keyword
        st.session_state.search_categories = categories
        st.session_state.search_regions = regions
        st.session_state.search_status = status
        if len(period) == 2:
            st.session_state.search_start_date, st.session_state.search_end_date = period
        st.session_state.search_urgent_only = urgent_only

    filters = _current_filters()
    summary = get_order_summary(filters)
    result = search_orders(filters)

    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("조회 건수", f"{int(summary['order_count']):,}건")
    c2.metric("총 주문 수량", f"{int(summary['total_quantity']):,}개")
    c3.metric("할인 반영 매출", f"{float(summary['total_amount']):,.0f}원")

    display = result.rename(columns={
        "id": "주문번호", "order_date": "주문일", "customer_name": "고객명",
        "product_name": "상품명", "category": "카테고리", "region": "지역",
        "quantity": "수량", "unit_price": "단가", "discount_rate": "할인율",
        "payment_method": "결제방법", "order_status": "처리상태",
        "urgent_order": "긴급주문", "attachment_name": "첨부파일",
    })
    visible = [
        "주문번호", "주문일", "고객명", "상품명", "카테고리", "지역",
        "수량", "단가", "할인율", "결제방법", "처리상태", "긴급주문", "첨부파일",
    ]
    st.dataframe(display[visible], use_container_width=True, hide_index=True)

    st.download_button(
        "조회 결과 CSV 다운로드",
        result.to_csv(index=False).encode("utf-8-sig"),
        "orders.csv", "text/csv",
    )
