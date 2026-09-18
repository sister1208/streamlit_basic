# app.py
import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(
    page_title="판매 주문 관리",
    page_icon="🛒",
    layout="wide"
)

# ---------------------------------------------------------
# 1. 세션 상태 초기화
# ---------------------------------------------------------
if "orders" not in st.session_state:
    st.session_state.orders = pd.DataFrame([
        {
            "주문번호": 1001,
            "주문일": date.today() - timedelta(days=3),
            "고객명": "김민수",
            "상품명": "노트북",
            "카테고리": "전자기기",
            "지역": "서울",
            "수량": 2,
            "단가": 1_200_000,
            "할인율": 5,
            "결제방법": "카드",
            "처리상태": "배송 중",
            "긴급주문": False
        },
        {
            "주문번호": 1002,
            "주문일": date.today() - timedelta(days=1),
            "고객명": "이서연",
            "상품명": "사무용 의자",
            "카테고리": "가구",
            "지역": "부산",
            "수량": 3,
            "단가": 180_000,
            "할인율": 0,
            "결제방법": "계좌이체",
            "처리상태": "주문 접수",
            "긴급주문": True
        }
    ])


PRODUCTS = {
    "노트북": ("전자기기", 1_200_000),
    "모니터": ("전자기기", 350_000),
    "키보드": ("전자기기", 80_000),
    "사무용 의자": ("가구", 180_000),
    "책상": ("가구", 250_000),
    "복사용지": ("사무용품", 30_000)
}

REGIONS = ["서울", "부산", "대구", "인천", "광주", "대전"]


# ---------------------------------------------------------
# 2. 화면 제목
# ---------------------------------------------------------
st.title("🛒 판매 주문 관리")


# ---------------------------------------------------------
# 3. segmented_control: 업무 화면 선택
# ---------------------------------------------------------
menu = st.segmented_control(
    "업무 선택",
    ["주문 조회", "주문 등록", "매출 분석"],
    default="주문 조회",
    key="main_menu"
)


# =========================================================
# 주문 조회
# =========================================================
if menu == "주문 조회":

    st.subheader("🔍 주문 검색")

    # form을 사용하면 입력할 때마다 재실행되지 않고,
    # 검색 버튼을 눌렀을 때 한 번에 처리됨
    with st.form("search_form"):

        col1, col2, col3 = st.columns(3)

        with col1:
            keyword = st.text_input(
                "고객명 또는 상품명",
                placeholder="예: 김민수, 노트북"
            )

            categories = st.multiselect(
                "카테고리",
                ["전자기기", "가구", "사무용품"],
                placeholder="전체 카테고리"
            )

        with col2:
            regions = st.multiselect(
                "지역",
                REGIONS,
                placeholder="전체 지역"
            )

            status = st.selectbox(
                "처리 상태",
                ["전체", "주문 접수", "배송 중", "배송 완료", "주문 취소"]
            )

        with col3:
            search_period = st.date_input(
                "주문 기간",
                value=(
                    date.today() - timedelta(days=30),
                    date.today()
                )
            )

            urgent_only = st.toggle(
                "긴급 주문만 조회",
                value=False
            )

        submitted = st.form_submit_button(
            "검색",
            type="primary",
            use_container_width=True
        )

    # 원본 데이터 복사
    filtered_df = st.session_state.orders.copy()

    if submitted:

        # 고객명 또는 상품명 검색
        if keyword:
            keyword_condition = (
                filtered_df["고객명"].str.contains(
                    keyword,
                    case=False,
                    na=False
                )
                |
                filtered_df["상품명"].str.contains(
                    keyword,
                    case=False,
                    na=False
                )
            )
            filtered_df = filtered_df[keyword_condition]

        # 카테고리 검색
        if categories:
            filtered_df = filtered_df[
                filtered_df["카테고리"].isin(categories)
            ]

        # 지역 검색
        if regions:
            filtered_df = filtered_df[
                filtered_df["지역"].isin(regions)
            ]

        # 처리 상태 검색
        if status != "전체":
            filtered_df = filtered_df[
                filtered_df["처리상태"] == status
            ]

        # 날짜 범위 검색
        if len(search_period) == 2:
            start_date, end_date = search_period

            filtered_df = filtered_df[
                (filtered_df["주문일"] >= start_date)
                &
                (filtered_df["주문일"] <= end_date)
            ]

        # 긴급 주문 검색
        if urgent_only:
            filtered_df = filtered_df[
                filtered_df["긴급주문"] == True
            ]

    st.divider()

    # 조회 결과 요약
    total_amount = (
        filtered_df["수량"] * filtered_df["단가"]
    ).sum()

    c1, c2, c3 = st.columns(3)

    c1.metric("조회 건수", f"{len(filtered_df):,}건")
    c2.metric("총 주문 수량", f"{filtered_df['수량'].sum():,}개")
    c3.metric("총 주문 금액", f"{total_amount:,.0f}원")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "주문일": st.column_config.DateColumn(
                "주문일",
                format="YYYY-MM-DD"
            ),
            "단가": st.column_config.NumberColumn(
                "단가",
                format="₩ %d"
            ),
            "할인율": st.column_config.NumberColumn(
                "할인율",
                format="%d%%"
            ),
            "긴급주문": st.column_config.CheckboxColumn(
                "긴급"
            )
        }
    )


# =========================================================
# 주문 등록
# =========================================================
elif menu == "주문 등록":

    st.subheader("📝 신규 주문 등록")

    with st.form(
        "order_form",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(2)

        with col1:
            customer_name = st.text_input(
                "고객명 *",
                placeholder="고객명을 입력하세요",
                max_chars=50
            )

            product_name = st.selectbox(
                "상품명 *",
                list(PRODUCTS.keys())
            )

            category, default_price = PRODUCTS[product_name]

            st.text_input(
                "카테고리",
                value=category,
                disabled=True
            )

            region = st.selectbox(
                "배송 지역 *",
                REGIONS
            )

        with col2:
            order_date = st.date_input(
                "주문일 *",
                value=date.today(),
                max_value=date.today()
            )

            quantity = st.number_input(
                "수량 *",
                min_value=1,
                max_value=1000,
                value=1,
                step=1
            )

            unit_price = st.number_input(
                "단가 *",
                min_value=0,
                value=default_price,
                step=10_000
            )

            discount_rate = st.slider(
                "할인율",
                min_value=0,
                max_value=30,
                value=0,
                step=1,
                format="%d%%"
            )

        payment_method = st.radio(
            "결제 방법",
            ["카드", "계좌이체", "현금", "후불 결제"],
            horizontal=True
        )

        urgent_order = st.checkbox(
            "긴급 주문으로 처리"
        )

        receive_message = st.toggle(
            "처리 결과 알림 수신",
            value=True
        )

        memo = st.text_area(
            "주문 메모",
            placeholder="배송 요청사항이나 기타 내용을 입력하세요.",
            height=100,
            max_chars=500
        )

        attachment = st.file_uploader(
            "발주서 또는 관련 문서",
            type=["pdf", "xlsx", "xls", "csv", "png", "jpg"]
        )

        # 실시간 계산식은 form 밖에서 사용하는 것이 더 자연스럽지만,
        # 여기서는 제출 시 최종 금액을 계산
        col_submit, col_reset = st.columns([3, 1])

        with col_submit:
            submitted = st.form_submit_button(
                "주문 등록",
                type="primary",
                use_container_width=True
            )

        with col_reset:
            cancelled = st.form_submit_button(
                "입력 취소",
                use_container_width=True
            )

    if submitted:

        # 입력값 검증
        errors = []

        if not customer_name.strip():
            errors.append("고객명을 입력하세요.")

        if quantity <= 0:
            errors.append("수량은 1개 이상이어야 합니다.")

        if unit_price <= 0:
            errors.append("단가는 0원보다 커야 합니다.")

        if errors:
            for error in errors:
                st.error(error)

        else:
            original_amount = quantity * unit_price
            discount_amount = original_amount * discount_rate / 100
            final_amount = original_amount - discount_amount

            next_id = (
                int(st.session_state.orders["주문번호"].max()) + 1
                if not st.session_state.orders.empty
                else 1001
            )

            new_order = pd.DataFrame([{
                "주문번호": next_id,
                "주문일": order_date,
                "고객명": customer_name.strip(),
                "상품명": product_name,
                "카테고리": category,
                "지역": region,
                "수량": quantity,
                "단가": unit_price,
                "할인율": discount_rate,
                "결제방법": payment_method,
                "처리상태": "주문 접수",
                "긴급주문": urgent_order
            }])

            st.session_state.orders = pd.concat(
                [st.session_state.orders, new_order],
                ignore_index=True
            )

            st.success(
                f"주문번호 {next_id}번이 등록되었습니다. "
                f"최종 결제금액은 {final_amount:,.0f}원입니다."
            )

            with st.expander("등록 결과 상세보기"):
                st.write("고객명:", customer_name)
                st.write("상품명:", product_name)
                st.write("원래 금액:", f"{original_amount:,.0f}원")
                st.write("할인 금액:", f"{discount_amount:,.0f}원")
                st.write("최종 금액:", f"{final_amount:,.0f}원")
                st.write("결제 방법:", payment_method)
                st.write("알림 수신:", "동의" if receive_message else "미동의")
                st.write("주문 메모:", memo or "없음")

                if attachment:
                    st.write("첨부파일:", attachment.name)


# =========================================================
# 매출 분석
# =========================================================
elif menu == "매출 분석":

    st.subheader("📊 매출 분석 조건")

    analysis_unit = st.segmented_control(
        "분석 기준",
        ["카테고리", "지역", "상품명"],
        default="카테고리"
    )

    top_n = st.slider(
        "상위 항목 개수",
        min_value=3,
        max_value=10,
        value=5
    )

    include_discount = st.checkbox(
        "할인 금액 반영",
        value=True
    )

    df = st.session_state.orders.copy()
    df["매출액"] = df["수량"] * df["단가"]

    if include_discount:
        df["매출액"] = (
            df["매출액"] *
            (1 - df["할인율"] / 100)
        )

    summary_df = (
        df.groupby(analysis_unit, as_index=False)["매출액"]
        .sum()
        .sort_values("매출액", ascending=False)
        .head(top_n)
    )

    st.bar_chart(
        summary_df,
        x=analysis_unit,
        y="매출액"
    )

    st.dataframe(
        summary_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "매출액": st.column_config.NumberColumn(
                "매출액",
                format="₩ %d"
            )
        }
    )