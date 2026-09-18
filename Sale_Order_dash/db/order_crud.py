import pandas as pd
import streamlit as st
from sqlalchemy import text

from config import ANALYSIS_COLUMNS
from db.connection import get_engine


SELECT_COLUMNS = """
    id, order_date, customer_name, product_name, category, region,
    quantity, unit_price, discount_rate, payment_method,
    order_status, urgent_order, receive_message, memo,
    attachment_name, created_at, updated_at
"""

# 캐시 삭제
def clear_order_cache():
    search_orders.clear()
    get_order_by_id.clear()
    get_order_summary.clear()
    get_sales_analysis.clear()

# 검색 화면에서 선택한 조건을 이용해 SQL의 WHERE 절과 바인딩 파라미터를 동적으로 만드는 함수
# : 모듈 내부에서 사용하는 보조 함수
def _build_search_conditions(filters):
    conditions = []
    params = {}

    keyword = filters.get("keyword", "").strip()
    if keyword:
        conditions.append(
            "(customer_name LIKE :keyword OR product_name LIKE :keyword)"
        )
        params["keyword"] = f"%{keyword}%"

    for field, values in (
        ("category", filters.get("categories", [])),
        ("region", filters.get("regions", [])),
    ):
        if values:
            placeholders = []
            for index, value in enumerate(values):
                key = f"{field}_{index}"
                placeholders.append(f":{key}")
                params[key] = value
            conditions.append(f"{field} IN ({', '.join(placeholders)})")

    status = filters.get("status", "전체")
    if status != "전체":
        conditions.append("order_status = :status")
        params["status"] = status

    start_date = filters.get("start_date")
    end_date = filters.get("end_date")
    if start_date and end_date:
        conditions.append("order_date BETWEEN :start_date AND :end_date")
        params.update({"start_date": start_date, "end_date": end_date})

    if filters.get("urgent_only"):
        conditions.append("urgent_order = TRUE")

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    return where_clause, params


############################################################
# order 테이블 CRUD
############################################################

# 주문 조회
@st.cache_data(ttl=60, show_spinner=False)
def search_orders(filters):
    where_clause, params = _build_search_conditions(filters)
    sql = text(f"""
        SELECT {SELECT_COLUMNS}
        FROM orders
        {where_clause}
        ORDER BY id DESC
    """)
    return pd.read_sql(sql, get_engine(), params=params)

# id 기준으로 주문 조회
@st.cache_data(ttl=60, show_spinner=False)
def get_order_by_id(order_id):
    sql = text(f"""
        SELECT {SELECT_COLUMNS}
        FROM orders
        WHERE id = :order_id
    """)
    with get_engine().connect() as connection:
        row = connection.execute(
            sql, {"order_id": int(order_id)}
        ).mappings().first()
        return dict(row) if row else None


# 주문 요약
@st.cache_data(ttl=60, show_spinner=False)
def get_order_summary(filters):
    where_clause, params = _build_search_conditions(filters)
    sql = text(f"""
        SELECT
            COUNT(*) AS order_count,
            COALESCE(SUM(quantity), 0) AS total_quantity,
            COALESCE(SUM(quantity * unit_price
                * (1 - discount_rate / 100)), 0) AS total_amount
        FROM orders
        {where_clause}
    """)
    return pd.read_sql(sql, get_engine(), params=params).iloc[0].to_dict()


# 신규 주문 등록
def insert_order(order):
    sql = text("""
        INSERT INTO orders (
            order_date, customer_name, product_name, category, region,
            quantity, unit_price, discount_rate, payment_method,
            order_status, urgent_order, receive_message, memo, attachment_name
        ) VALUES (
            :order_date, :customer_name, :product_name, :category, :region,
            :quantity, :unit_price, :discount_rate, :payment_method,
            :order_status, :urgent_order, :receive_message, :memo, :attachment_name
        )
    """)
    with get_engine().begin() as connection:
        order_id = connection.execute(sql, order).lastrowid
    clear_order_cache()
    return order_id


# 주문 정보 수정
def update_order(order_id, order):
    params = {**order, "order_id": int(order_id)}
    sql = text("""
        UPDATE orders
        SET order_date=:order_date,
            customer_name=:customer_name,
            product_name=:product_name,
            category=:category,
            region=:region,
            quantity=:quantity,
            unit_price=:unit_price,
            discount_rate=:discount_rate,
            payment_method=:payment_method,
            order_status=:order_status,
            urgent_order=:urgent_order,
            receive_message=:receive_message,
            memo=:memo,
            attachment_name=:attachment_name
        WHERE id=:order_id
    """)
    with get_engine().begin() as connection:
        rowcount = connection.execute(sql, params).rowcount
    clear_order_cache()
    return rowcount

# 주문 정보 삭제
def delete_order(order_id):
    with get_engine().begin() as connection:
        rowcount = connection.execute(
            text("DELETE FROM orders WHERE id=:order_id"),
            {"order_id": int(order_id)},
        ).rowcount
    clear_order_cache()
    return rowcount


# 매출 분석
@st.cache_data(ttl=60, show_spinner=False)
def get_sales_analysis(group_label, top_n, include_discount):
    group_column = ANALYSIS_COLUMNS[group_label]
    amount_expression = "quantity * unit_price"
    if include_discount:
        amount_expression += " * (1 - discount_rate / 100)"

    # group_column은 config.py의 화이트리스트에서만 선택
    sql = text(f"""
        SELECT {group_column} AS analysis_group,
               SUM({amount_expression}) AS sales_amount
        FROM orders
        GROUP BY {group_column}
        ORDER BY sales_amount DESC
        LIMIT :top_n
    """)
    return pd.read_sql(sql, get_engine(), params={"top_n": int(top_n)})
