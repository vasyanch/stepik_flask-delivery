import datetime
from collections import Counter

from flask import render_template, request, session, redirect, url_for

from app import app, db
from forms import OrderForm, LoginForm, RegisterForm
from models import User, Category, Dish, Order, DishesInOrder


@app.route('/')
def render_index():
    categories = Category.query.all()
    categories_for_template = {
        category.id: {
            'title': category.title,
            'dishes':
                Dish.query.join(Dish.categories).filter(Category.id == category.id).order_by(db.func.random()).limit(3)
        }
        for category in categories
    }
    categories_for_template = sorted(list(categories_for_template.items()), key=lambda x: x[0])
    cart_for_template = get_cart_for_template(session)
    return render_template('index.html', categories=categories_for_template, cart=cart_for_template, session=session)


@app.route('/cart/', methods=['POST', 'GET'])
def render_cart():
    error = ''
    del_item_message = ''
    if session.get('del_item_message'):
        del_item_message = 'Блюдо удалено из корзины'
        session.pop('del_item_message')
    order_form = OrderForm()
    cart = session.get('cart')
    ordered_dishes = Dish.query.filter(Dish.id.in_(cart)).all() if cart else []
    counter = Counter(cart) if cart else {}
    ordered_dishes = [{'dish': dish, 'amount': counter[dish.id]} for dish in ordered_dishes]
    if request.method == 'POST' and order_form.validate_on_submit():
        if not cart:
            error = 'Для того чтобы сделать заказ в корзине должен быть хотя бы один товар'
        else:
            dishes_in_order = [DishesInOrder(amount=item['amount'], dish=item['dish']) for item in ordered_dishes]

            order = Order(
                date=datetime.datetime.now(),
                status='accepted',
                order_sum=session.get('cart_sum'),
                name=order_form.name.data,
                email=order_form.email.data,
                phone=order_form.phone.data,
                address=order_form.address.data,
                dishes=dishes_in_order,
                user_id=session.get('user')['id'] if session.get('user') else None
            )
            db.session.add_all(dishes_in_order)
            db.session.add(order)
            db.session.commit()
            return redirect(url_for('render_ordered'))
    cart_for_template = get_cart_for_template(session)
    return render_template(
        'cart.html', error=error, message=del_item_message, ordered_dishes=ordered_dishes, cart=cart_for_template,
        form=order_form, session=session
    )


@app.route('/account/')
def render_account():
    user = session.get('user')
    error = ''
    if user:
        user = User.query.get(user['id'])
        orders = Order.query.filter_by(user_id=user.id).order_by(Order.date.desc())
    else:
        orders = []
        error = 'Личный кабинет доступен только для зарегистрированных пользователей'
    cart = get_cart_for_template(session)
    return render_template('account.html', orders=orders, error=error, cart=cart, session=session)


@app.route('/login/', methods=['GET', 'POST'])
def render_login():
    error = ''
    login_form = LoginForm()
    if request.method == 'POST' and login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        user = User.query.filter_by(email=email).first()
        if user and user.password_valid(password):
            session['user'] = {'id': user.id, 'email': user.email}
            return redirect(url_for('render_account'))
        else:
            error = "Неправильный логин или пароль"
    cart_for_template = get_cart_for_template(session)
    return render_template('login.html', error=error, cart=cart_for_template, form=login_form, session=session)


@app.route('/register/', methods=['GET', 'POST'])
def render_register():
    error = ''
    register_form = RegisterForm()
    if request.method == "POST" and register_form.validate_on_submit():
        new_user = User(
            email=register_form.email.data,
            password=register_form.password.data
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('render_index'))
    cart_for_template = get_cart_for_template(session)
    return render_template('register.html', error=error, cart=cart_for_template, form=register_form, session=session)


@app.route('/logout/')
def render_logout():
    session.clear()
    return redirect(url_for('render_index'))


@app.route('/ordered/')
def render_ordered():
    if session.get('cart'):
        session.pop('cart')
        session.pop('cart_sum')
    return render_template('ordered.html', session=session)


@app.route('/admin/')
def render_admin():
    return render_template('')


@app.route('/add_to_cart/<int:dish_id>')
def render_add_to_cart(dish_id):
    cart = session.get('cart', [])
    cart_sum = session.get('cart_sum', 0)
    cart.append(dish_id)
    session['cart'] = cart
    cart_sum += Dish.query.get(dish_id).price
    session['cart_sum'] = cart_sum
    return redirect(url_for('render_cart'))


@app.route('/remove_from_cart/<int:dish_id>')
def render_remove_from_cart(dish_id):
    cart = session.get('cart')
    cart.remove(dish_id)
    session['cart_sum'] -= Dish.query.get(dish_id).price
    session['cart'] = cart
    session['del_item_message'] = True
    return redirect(url_for('render_cart'))


def get_cart_for_template(session_obj):
    cart = session_obj.get('cart')
    if cart:
        cart_len = len(cart)
        if cart_len == 1:
            amount_dishes = f'{cart_len} блюдо'
        elif cart_len < 5:
            amount_dishes = f'{cart_len} блюда'
        else:
            amount_dishes = f'{cart_len} блюд'
        cart_for_template = {'amount_dishes': amount_dishes, 'cart_sum': session['cart_sum']}
    else:
        cart_for_template = None
    return cart_for_template
