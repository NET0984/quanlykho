
from decimal import Decimal

LOW_STOCK_THRESHOLD = Decimal('10')


def normalize_quantity(quantity):
    if quantity is None:
        return Decimal('0')
    if isinstance(quantity, Decimal):
        return quantity
    return Decimal(str(quantity))


def get_stock_status(quantity):
    qty = normalize_quantity(quantity)
    if qty <= 0:
        return 'OUT'
    if qty <= LOW_STOCK_THRESHOLD:
        return 'LOW'
    return 'IN'


def get_stock_status_label(quantity):
    status = get_stock_status(quantity)
    return {
        'OUT': 'Hết hàng',
        'LOW': 'Sắp hết',
        'IN': 'Còn hàng',
    }[status]


def build_stock_payload(quantity):
    qty = normalize_quantity(quantity)
    return {
        'stock_quantity': qty,
        'stock_status': get_stock_status(qty),
        'stock_status_label': get_stock_status_label(qty),
    }
