from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_model import Base, User, ComputerShop, Product

app = Flask(__name__)

engine = create_engine('sqlite:///computer_shop.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route("/")
@app.route("/shops")
def entry_point():
    shops = session.query(ComputerShop).all()
    return render_template('index.html', shops=shops)


@app.route("/shop/new")
def create_new_shop():
    return 'create new shop'


@app.route("/shop/<int:shop_id>")
def get_shop(shop_id):
    shop = session.query(ComputerShop).filter_by(id=shop_id).one()
    products = session.query(Product).filter_by(computer_shop_id=shop.id).all()
    return render_template('shop.html', shop=shop, products=products)


@app.route("/shop/<int:shop_id>/edit", methods=["GET", "POST"])
def edit_shop(shop_id):
    shop = session.query(ComputerShop).filter_by(id=shop_id).one()
    if request.method == 'POST':
        if request.form['name']:
            shop.name = request.form['name']
            session.add(shop)
            session.commit()
        return redirect(url_for('get_shop', shop_id=shop_id))
    else:
        return render_template('shop-edit.html', shop=shop)


@app.route("/shop/<int:shop_id>/delete")
def delete_shop(shop_id):
    return 'delete shop with shop id {}'.format(shop_id)


@app.route("/shop/<int:shop_id>/product/new")
def create_product(shop_id):
    return 'create product for ship_id {}'.format(shop_id)


@app.route("/shop/<int:shop_id>/product/<int:product_id>")
def get_product(shop_id, product_id):
    shop = session.query(ComputerShop).filter_by(id=shop_id).one()
    product = session.query(Product).filter_by(id=product_id).one()
    return render_template('product.html', shop=shop, product=product)


@app.route("/shop/<int:shop_id>/product/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product(shop_id, product_id):
    shop = session.query(ComputerShop).filter_by(id=shop_id).one()
    product = session.query(Product).filter_by(id=product_id).one()
    if request.method == 'POST':
        product.name = request.form["name"]
        product.description = request.form["description"]
        product.price = request.form["price"]
        session.add(product)
        session.commit()
        return redirect(url_for('get_product', shop_id=shop_id, product_id=product_id))
    else:
        return render_template('product-edit.html', shop=shop, product=product)


@app.route("/shop/<int:shop_id>/product/<int:product_id>/delete")
def delete_product(shop_id, product_id):
    return 'delete product with product_id {0} and shop_id {1}'.format(product_id, shop_id)


if __name__ == "__main__":
    app.debug = True
    app.run(port=8080)
