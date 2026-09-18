import pandas as pd
import streamlit as st

from db.order_crud import delete_order, get_order_by_id
from services.order_service import modify_order
from ui.order_form import render_order_fields


def render_manage_view():
    st.subheader("✏️ 주문 수정·삭제")

    col1, col2 = st.columns([3, 1])
    order_id = col1.number_input("주문번호", min_value=1, step=1)
    load = col2.button("DB에서 불러오기", use_container_width=True)
    if load:
        st.session_state.selected_order_id = int(order_id)

    selected_id = st.session_state.selected_order_id
    if not selected_id:
        st.info("수정하거나 삭제할 주문번호를 입력한 후 불러오세요.")
        return

    order = get_order_by_id(selected_id)
    if not order:
        st.warning("해당 주문번호의 데이터가 없습니다.")
        st.session_state.selected_order_id = None
        return

    order["order_date"] = pd.to_datetime(order["order_date"]).date()
    edited_order = render_order_fields(f"edit_{selected_id}", order, allow_status=True)

    update_col, delete_col = st.columns(2)
    if update_col.button("DB 수정", type="primary", use_container_width=True):
        try:
            rowcount, errors = modify_order(selected_id, edited_order)
            if errors:
                for error in errors:
                    st.error(error)
            elif rowcount:
                st.session_state.flash_message = f"주문번호 {selected_id}번이 수정되었습니다."
                st.rerun()
            else:
                st.info("변경된 데이터가 없습니다.")
        except Exception as error:
            st.error(f"수정 실패: {error}")

    with delete_col.popover("주문 삭제", use_container_width=True):
        st.warning("삭제한 주문은 복구할 수 없습니다.")
        confirmed = st.checkbox("삭제 내용을 확인했습니다.")
        if st.button("MySQL에서 삭제", disabled=not confirmed, type="primary"):
            try:
                if delete_order(selected_id):
                    st.session_state.selected_order_id = None
                    st.session_state.flash_message = f"주문번호 {selected_id}번이 삭제되었습니다."
                    st.rerun()
                else:
                    st.info("이미 삭제되었거나 존재하지 않는 주문입니다.")
            except Exception as error:
                st.error(f"삭제 실패: {error}")
