from datetime import date

import streamlit as st

from config import ORDER_STATUSES, PAYMENT_METHODS, PRODUCTS, REGIONS


def render_order_fields(prefix, initial=None, allow_status=False):
    """등록·수정 화면에서 공통으로 사용하는 주문 입력 위젯."""
    initial = initial or {}
    product_names = list(PRODUCTS.keys())
    selected_product = initial.get("product_name", product_names[0])
    product_index = product_names.index(selected_product)

    col1, col2 = st.columns(2)
    with col1:
        customer_name = st.text_input(
            "고객명 *", value=initial.get("customer_name", ""),
            max_chars=50, key=f"{prefix}_customer_name",
        )
        product_name = st.selectbox(
            "상품명 *", product_names, index=product_index,
            key=f"{prefix}_product_name",
        )
        category, default_price = PRODUCTS[product_name]
        st.text_input(
            "카테고리", value=category, disabled=True,
            key=f"{prefix}_category",
        )
        region = st.selectbox(
            "배송 지역 *", REGIONS,
            index=REGIONS.index(initial.get("region", REGIONS[0])),
            key=f"{prefix}_region",
        )

    with col2:
        order_date = st.date_input(
            "주문일 *", value=initial.get("order_date", date.today()),
            key=f"{prefix}_order_date",
        )
        quantity = st.number_input(
            "수량 *", min_value=1, max_value=1000,
            value=int(initial.get("quantity", 1)), step=1,
            key=f"{prefix}_quantity",
        )
        unit_price = st.number_input(
            "단가 *", min_value=0,
            value=int(initial.get("unit_price", default_price)), step=10_000,
            key=f"{prefix}_unit_price",
        )
        discount_rate = st.slider(
            "할인율", min_value=0, max_value=30,
            value=int(initial.get("discount_rate", 0)), step=1,
            format="%d%%", key=f"{prefix}_discount_rate",
        )

    payment_method = st.radio(
        "결제 방법", PAYMENT_METHODS,
        index=PAYMENT_METHODS.index(initial.get("payment_method", PAYMENT_METHODS[0])),
        horizontal=True, key=f"{prefix}_payment_method",
    )
    order_status = initial.get("order_status", ORDER_STATUSES[0])
    if allow_status:
        order_status = st.selectbox(
            "처리 상태", ORDER_STATUSES,
            index=ORDER_STATUSES.index(order_status),
            key=f"{prefix}_order_status",
        )

    urgent_order = st.checkbox(
        "긴급 주문으로 처리", value=bool(initial.get("urgent_order", False)),
        key=f"{prefix}_urgent_order",
    )
    receive_message = st.toggle(
        "처리 결과 알림 수신", value=bool(initial.get("receive_message", True)),
        key=f"{prefix}_receive_message",
    )
    memo = st.text_area(
        "주문 메모", value=initial.get("memo") or "", max_chars=500,
        key=f"{prefix}_memo",
    )
    attachment = st.file_uploader(
        "발주서 또는 관련 문서",
        type=["pdf", "xlsx", "xls", "csv", "png", "jpg"],
        key=f"{prefix}_attachment",
    )
    attachment_name = attachment.name if attachment else initial.get("attachment_name")

    return {
        "order_date": order_date,
        "customer_name": customer_name.strip(),
        "product_name": product_name,
        "category": category,
        "region": region,
        "quantity": int(quantity),
        "unit_price": int(unit_price),
        "discount_rate": int(discount_rate),
        "payment_method": payment_method,
        "order_status": order_status,
        "urgent_order": bool(urgent_order),
        "receive_message": bool(receive_message),
        "memo": memo.strip() or None,
        "attachment_name": attachment_name,
    }
