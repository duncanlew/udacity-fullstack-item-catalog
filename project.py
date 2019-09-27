from flask import Flask, render_template, request, redirect, url_for, session as flask_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_model import Base, User, ComputerShop, Product

app = Flask(__name__)
app.secret_key = "super secret key"

engine = create_engine('sqlite:///computer_shop.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()


# TODO rename entry_point to home
@app.route("/")
@app.route("/shops")
def entry_point():
    shops = db_session.query(ComputerShop).all()
    return render_template('index.html', shops=shops)


@app.route("/shop/new", methods=["GET", "POST"])
def create_shop():
    # TODO user authentication needs to be created
    user = db_session.query(User).filter_by(id=1).one()

    if request.method == 'POST':
        if request.form['name']:
            new_shop = ComputerShop(name=request.form['name'], user=user)
            db_session.add(new_shop)
            db_session.commit()
        return redirect(url_for('entry_point'))
    else:
        return render_template('shop-new.html')


@app.route("/shop/<int:shop_id>")
def get_shop(shop_id):
    shop = db_session.query(ComputerShop).filter_by(id=shop_id).one()
    products = db_session.query(Product).filter_by(computer_shop_id=shop.id).all()
    return render_template('shop.html', shop=shop, products=products)


@app.route("/shop/<int:shop_id>/edit", methods=["GET", "POST"])
def edit_shop(shop_id):
    shop = db_session.query(ComputerShop).filter_by(id=shop_id).one()
    if request.method == 'POST':
        if request.form['name']:
            shop.name = request.form['name']
            db_session.add(shop)
            db_session.commit()
        return redirect(url_for('get_shop', shop_id=shop_id))
    else:
        return render_template('shop-edit.html', shop=shop)


@app.route("/shop/<int:shop_id>/delete", methods=["GET", "POST"])
def delete_shop(shop_id):
    # TODO user authentication needs to be created
    user = db_session.query(User).filter_by(id=1).one()
    shop = db_session.query(ComputerShop).filter_by(id=shop_id).one()
    if request.method == 'POST':
        db_session.delete(shop)
        db_session.commit()
        return redirect(url_for('entry_point'))
    else:
        return render_template('shop-delete.html', shop=shop)


@app.route("/shop/<int:shop_id>/product/new", methods=["GET", "POST"])
def create_product(shop_id):
    # TODO user authentication needs to be created
    user = db_session.query(User).filter_by(id=1).one()
    shop = db_session.query(ComputerShop).filter_by(id=shop_id).one()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        new_product = Product(name=name, description=description, price=price,
                              computer_shop=shop)
        db_session.add(new_product)
        db_session.commit()
        return redirect(url_for('get_shop', shop_id=shop.id))
    else:
        return render_template('product-new.html', shop=shop)


@app.route("/shop/<int:shop_id>/product/<int:product_id>")
def get_product(shop_id, product_id):
    shop = db_session.query(ComputerShop).filter_by(id=shop_id).one()
    product = db_session.query(Product).filter_by(id=product_id).one()
    return render_template('product.html', shop=shop, product=product)


@app.route("/shop/<int:shop_id>/product/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product(shop_id, product_id):
    shop = db_session.query(ComputerShop).filter_by(id=shop_id).one()
    product = db_session.query(Product).filter_by(id=product_id).one()
    if request.method == 'POST':
        product.name = request.form["name"]
        product.description = request.form["description"]
        product.price = request.form["price"]
        db_session.add(product)
        db_session.commit()
        return redirect(url_for('get_product', shop_id=shop_id, product_id=product_id))
    else:
        return render_template('product-edit.html', shop=shop, product=product)


@app.route("/shop/<int:shop_id>/product/<int:product_id>/delete", methods=["GET", "POST"])
def delete_product(shop_id, product_id):
    # TODO user authentication needs to be created
    user = db_session.query(User).filter_by(id=1).one()
    shop = db_session.query(ComputerShop).filter_by(id=shop_id).one()
    product = db_session.query(Product).filter_by(id=product_id).one()
    if request.method == 'POST':
        db_session.delete(product)
        db_session.commit()
        return redirect(url_for('get_shop', shop_id=shop.id))
    else:
        return render_template('product-delete.html', shop=shop, product=product)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_incorrect = False
    if request.method == "POST":
        username = request.form['email']
        password = request.form['password']
        user = db_session.query(User).filter_by(username=username).first()
        if not user or not user.verify_password(password):
            login_incorrect = True
            return render_template('login.html', login_incorrect=login_incorrect)
        else:
            flask_session['username'] = username
            return '<h1>Login successful!</h1><div>{0}</div>'.format(username)
    else:
        if 'username' in flask_session:
            username = flask_session['username']
            return '<h1>Hello {0}, you\'re already logged in</h1>'.format(username)
        else:
            return render_template('login.html', login_incorrect=login_incorrect)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    flask_session.pop('username', None)
    return redirect(url_for('entry_point'))


if __name__ == "__main__":
    app.debug = True
    app.run(port=8080)
