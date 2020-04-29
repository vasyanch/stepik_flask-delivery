from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    orders = db.relationship('Order', back_populates='user')

    @property
    def password(self):
        raise AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        return check_password_hash(self.password_hash, password)


dish_category_association_table = db.Table(
    'dish_category_association', db.metadata,
    db.Column('Dish', db.Integer, db.ForeignKey('dishes.id'), nullable=False),
    db.Column('Category', db.Integer, db.ForeignKey('categories.id'), nullable=False)
)


class DishesInOrder(db.Model):
    __tablename__ = 'dishs_in_order'
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'), primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    amount = db.Column(db.Integer, nullable=True)
    dish = db.relationship('Dish', back_populates='orders')
    order = db.relationship('Order', back_populates='dishes')


class Dish(db.Model):
    __tablename__ = 'dishes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)
    categories = db.relationship('Category', secondary=dish_category_association_table, back_populates='dishes')
    orders = db.relationship('DishesInOrder', back_populates='dish')


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    dishes = db.relationship('Dish', secondary=dish_category_association_table, back_populates='categories')


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    order_sum = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    dishes = db.relationship('DishesInOrder', back_populates='order')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='orders')

    def get_str_date(self):
        return self.date.strftime('%d.%m.%y')
