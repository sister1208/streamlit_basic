from datetime import date, timedelta

import streamlit as st


def init_session_state():
    """세션에는 DB 데이터가 아닌 화면 상태와 검색 조건만 저장한다."""
    defaults = {
        "main_menu": "주문 조회",
        "search_keyword": "",
        "search_categories": [],
        "search_regions": [],
        "search_status": "전체",
        "search_start_date": date.today() - timedelta(days=30),
        "search_end_date": date.today(),
        "search_urgent_only": False,
        "selected_order_id": None,
        "flash_message": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def show_flash_message():
    message = st.session_state.pop("flash_message", None)
    if message:
        st.success(message)
