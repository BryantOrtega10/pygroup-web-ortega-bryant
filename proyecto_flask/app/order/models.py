from datetime import datetime
from pprint import pprint

from sqlalchemy import func

from app.db import db, ma
from app.products.models import Product, Stock


class RefOrderStatusCode(db.Model):
    order_status_code = db.Column(db.Integer, primary_key=True)
    order_status_description = db.Column(db.String(100))


class Order(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    order_status_code = db.Column(db.Integer, db.ForeignKey('ref_order_status_code.order_status_code'))
    date_created = db.Column(db.DateTime, default=datetime.now())
    order_details = db.Column(db.String(20), default="")


class RefOrderItemStatusCode(db.Model):
    order_item_status_code = db.Column(db.Integer, primary_key=True)
    order_item_status_description = db.Column(db.String(100))


class OrderItem(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    order_id = db.Column(db.String(20), db.ForeignKey('order.id'))
    order_item_status_code = db.Column(db.Integer, db.ForeignKey('ref_order_item_status_code.order_item_status_code'))
    order_item_quantity = db.Column(db.Integer)
    order_item_price = db.Column(db.Integer)
    order_order_item_details = db.Column(db.String(20), default="")


class RefInvoiceStatusCode(db.Model):
    invoice_status_code = db.Column(db.Integer, primary_key=True)
    invoice_status_description = db.Column(db.String(100))


class Invoice(db.Model):
    number = db.Column(db.Numeric, primary_key=True)
    order_id = db.Column(db.String(100), db.ForeignKey('order.id'))
    invoice_status_code = db.Column(db.Integer, db.ForeignKey('ref_invoice_status_code.invoice_status_code'))
    invoice_date = db.Column(db.DateTime, default=datetime.now())
    invoice_detail_address = db.Column(db.String(100))
    customer_payment_method_id = db.Column(db.Integer, db.ForeignKey('customer_payment_method.id'))


def get_order_active_by_customer(customer_id):
    order = Order.query.filter_by(customer_id=customer_id, order_status_code=1).first()
    if order:
        order_items = db.session.query(OrderItem, Product, Stock) \
            .filter_by(order_id=order.id, order_item_status_code=1) \
            .filter(OrderItem.product_id == Product.id).filter(Stock.product_id == Product.id).all()
        return order, order_items
    return None, None


def get_subtotal_by_customer(customer_id):
    order = Order.query.filter_by(customer_id=customer_id, order_status_code=1).first()
    if order:
        order_items = OrderItem.query.with_entities(func.sum(OrderItem.order_item_price).label('sumatory')).filter_by(
            order_id=order.id, order_item_status_code=1).all()
        return order_items[0].sumatory
    return 0


def create_new_order(customer_id):
    number_of_orders = Order.query.filter_by(customer_id=customer_id).count()
    order_id = "ORD_" + str(customer_id) + "_" + str(number_of_orders + 1)
    order = Order(id=order_id, customer_id=customer_id, order_status_code=1)
    db.session.add(order)
    db.session.commit()
    return order


def create_order_item(product_id, order_id, order_item_status_code, order_item_quantity, order_item_price):
    order_item_id = "ORD_ITEM_" + str(order_id) + "_" + str(product_id)
    order_item = OrderItem(id=order_item_id, product_id=product_id, order_id=order_id,
                           order_item_status_code=order_item_status_code,
                           order_item_quantity=order_item_quantity, order_item_price=order_item_price)
    db.session.add(order_item)
    db.session.commit()
    return order_item


def update_order_item(order_item_id, order_item_quantity, order_item_price, order_item_status_code):
    order_item = OrderItem.query.filter_by(id=order_item_id).first()
    order_item.order_item_quantity = order_item_quantity
    order_item.order_item_price = order_item_price
    order_item.order_item_status_code = order_item_status_code
    db.session.add(order_item)
    db.session.commit()
    return order_item


def delete_order_item(order_item_id):
    order_item = OrderItem.query.filter_by(id=order_item_id).first()
    order_item.order_item_status_code = 2
    db.session.add(order_item)
    db.session.commit()
    return True


def create_invoice_by_order_id(order_id, address, payment_id):
    order = Order.query.filter_by(id=order_id).first()
    number_of_invoices = db.session.query(Invoice, Order) \
        .filter(Order.customer_id == order.customer_id) \
        .filter(Invoice.order_id == Order.id).count()

    invoice = Invoice(number=(number_of_invoices + 1), order_id=order_id, invoice_status_code=1,
                      invoice_detail_address=address,
                      customer_payment_method_id=payment_id)
    order.order_status_code = 3
    db.session.add(invoice)
    db.session.add(order)
    db.session.commit()
    return invoice


def get_invoice_by_id(id):
    invoice = Invoice.query.filter_by(number=id).first()
    return invoice


def get_order_items_by_order_id(order_id):
    order_items = db.session.query(OrderItem, Product) \
        .filter_by(order_id=order_id) \
        .filter(OrderItem.product_id == Product.id).all()
    return order_items


def get_subtotal_by_order_id(order_id):
    order_items = OrderItem.query.with_entities(func.sum(OrderItem.order_item_price).label('sumatory')).filter_by(
        order_id=order_id, order_item_status_code=1).all()
    print(order_items)

    return order_items[0].sumatory
