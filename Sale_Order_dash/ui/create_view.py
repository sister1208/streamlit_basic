import streamlit as st

from services.order_service import calculate_amount, create_order
from ui.order_form import render_order_fields


def render_create_view():
    st.subheader("📝 신규 주문 등록")
    order = render_order_fields("create")

    original, discount, final = calculate_amount(
        order["quantity"], order["unit_price"], order["discount_rate"]
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("주문 금액", f"{original:,.0f}원")
    c2.metric("할인 금액", f"{discount:,.0f}원")
    c3.metric("최종 금액", f"{final:,.0f}원")

    if st.button("DB에 주문 등록", type="primary", use_container_width=True):
        try:
            order_id, errors = create_order(order)
            if errors:
                for error in errors:
                    st.error(error)
            else:
                st.success(f"주문번호 {order_id}번이 MySQL에 저장되었습니다.")
        except Exception as error:
            st.error(f"주문 등록 실패: {error}")
