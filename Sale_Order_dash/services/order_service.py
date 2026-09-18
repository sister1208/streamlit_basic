from db.order_crud import insert_order, update_order


def validate_order(order):
    errors = []
    if not order["customer_name"].strip():
        errors.append("고객명을 입력하세요.")
    if order["quantity"] < 1:
        errors.append("수량은 1개 이상이어야 합니다.")
    if order["unit_price"] <= 0:
        errors.append("단가는 0원보다 커야 합니다.")
    if not 0 <= order["discount_rate"] <= 100:
        errors.append("할인율은 0~100 사이여야 합니다.")
    return errors


def calculate_amount(quantity, unit_price, discount_rate):
    original = quantity * unit_price
    discount = original * discount_rate / 100
    return original, discount, original - discount


def create_order(order):
    errors = validate_order(order)
    if errors:
        return None, errors
    return insert_order(order), []


def modify_order(order_id, order):
    errors = validate_order(order)
    if errors:
        return 0, errors
    return update_order(order_id, order), []
