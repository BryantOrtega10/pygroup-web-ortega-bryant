from datetime import datetime
from flask import jsonify
from app.db import db, ma
from app.products.exceptions import ModelNotFoundError

class Product(db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(500), default="https://www.saccon.it/img/coming-soon.jpg")
    price = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, default=1)
    description = db.Column(db.String(500), nullable=True)
    refundable = db.Column(db.Boolean, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        fields = ["id", "name", "image", "description", "price", "refundable"]


class Category(db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        fields = ["id", "name"]

class Stock(db.Model):
    """
    """
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())

class StockSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Stock
        fields = ["id", "product_id", "quantity"]

def get_all_categories():
    categories = Category.query.all()
    category_schema = CategorySchema()
    categories = [category_schema.dump(category) for category in categories]
    return categories


def create_new_category(name):
    category = Category(name=name)
    db.session.add(category)

    db.session.commit()
    return category


def get_stock_by_product(product_id):
    stock = Stock.query.filter_by(product_id=product_id).first()
    stock_schema = StockSchema()
    return stock_schema.dump(stock)


def get_products_with_low_stock():
    stock = Stock.query.filter_by(Stock.quantity <= 5).first()
    stock_schema = StockSchema()
    return stock_schema.dump(stock)


def get_all_products():
    products_qs = Product.query.all()
    product_schema = ProductSchema()
    products_serialization = [product_schema.dump(product) for product in
                              products_qs]

    return products_serialization


def get_product_by_id(id):
    product_qs = Product.query.filter_by(id=id).first()
    if product_qs:
        product_schema = ProductSchema()
        p = product_schema.dump(product_qs)
        return p
    else:
        raise ModelNotFoundError

def create_new_product(name, image, price, weight, description, refundable, category_id):

    product = Product(name=name, image=image, price=price, weight=weight, description=description, refundable=refundable, category_id=category_id)
    db.session.add(product)
    if db.session.commit():
        return product
    return None

def create_new_stock(product_id, quantity):
    stockFil = Stock.query.filter_by(product_id=product_id).first()
    if stockFil == None:
        stock = Stock(product_id=product_id, quantity=quantity)
        db.session.add(stock)
        if db.session.commit():
            return stock

    return None
    
def update_stock(product_id, quantity):
    stock = Stock.query.filter_by(product_id=product_id).first()
    if stock != None:
        stock.quantity = quantity
        db.session.commit()
        stock_schema = StockSchema()
        return stock_schema.dump(stock)
    return None


def get_all_products_by_cat(category_id):
    products_qs = Product.query.filter_by(category_id=category_id).all()
    product_schema = ProductSchema()
    products_serialization = [product_schema.dump(product) for product in
                              products_qs]

    return products_serialization


def get_category_by_id(category_id):
    category = Category.query.filter_by(id=category_id).first()
    category_schema = CategorySchema()
    category_ob = category_schema.dump(category)
    return category_ob
