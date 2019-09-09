from flask import Flask, render_template
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
    return render_template('index.html')


@app.route("/shop/new")
def create_new_shop():
    return 'create new shop'


@app.route("/shop/<int:shop_id>")
def get_shop(shop_id):
    return 'display shop with shop id {}'.format(shop_id)


@app.route("/shop/<int:shop_id>/edit")
def edit_shop(shop_id):
    return 'edit shop with shop id {}'.format(shop_id)


@app.route("/shop/<int:shop_id>/delete")
def delete_shop(shop_id):
    return 'delete shop with shop id {}'.format(shop_id)


@app.route("/shop/<int:shop_id>/product/new")
def create_product(shop_id):
    return 'create product for ship_id {}'.format(shop_id)


@app.route("/shop/<int:shop_id>/product/<int:product_id>")
def get_product(shop_id, product_id):
    return 'get product with product_id {0} and shop_id {1}'.format(product_id, shop_id)


@app.route("/shop/<int:shop_id>/product/<int:product_id>/edit")
def edit_product(shop_id, product_id):
    return 'edit product with product_id {0} and shop_id {1}'.format(product_id, shop_id)


@app.route("/shop/<int:shop_id>/product/<int:product_id>/delete")
def delete_product(shop_id, product_id):
    return 'delete product with product_id {0} and shop_id {1}'.format(product_id, shop_id)


if __name__ == "__main__":
    app.debug = True
    app.run(port=8080)
