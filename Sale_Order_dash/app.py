import streamlit as st

from config import MENU_ITEMS
from db.connection import test_connection
from ui.analysis_view import render_analysis_view
from ui.create_view import render_create_view
from ui.manage_view import render_manage_view
from ui.search_view import render_search_view
from utils.state import init_session_state, show_flash_message


st.set_page_config(
    page_title="판매 주문 관리",
    page_icon="🛒",
    layout="wide",
)

init_session_state()

st.title("🛒 판매 주문 관리")
st.caption("Streamlit Input Widget + SQLAlchemy + MySQL 실무형 예제")
show_flash_message()

try:
    test_connection()
except Exception as error:
    st.error(f"MySQL 연결 실패: {error}")
    st.stop()

menu = st.segmented_control(
    "업무 선택",
    MENU_ITEMS,
    key="main_menu",
)

views = {
    "주문 조회": render_search_view,
    "주문 등록": render_create_view,
    "주문 수정·삭제": render_manage_view,
    "매출 분석": render_analysis_view,
}
views[menu]()
