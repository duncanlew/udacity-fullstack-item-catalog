from flask import Flask, g, render_template, request, redirect, url_for, session as flask_session, abort
from flask_oauthlib.client import OAuth
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import wraps

from database_model import Base, User, ComputerShop, Product

app = Flask(__name__)
app.secret_key = "super secret key"
oauth = OAuth()

engine = create_engine('sqlite:///computer_shop.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

twitter = oauth.remote_app('twitter',
                           base_url='https://api.twitter.com/1/',
                           request_token_url='https://api.twitter.com/oauth/request_token',
                           access_token_url='https://api.twitter.com/oauth/access_token',
                           authorize_url='https://api.twitter.com/oauth/authenticate',
                           consumer_key='YOUR_CONSUMER_KEY',
                           consumer_secret='YOUR_CONSUMER_SECRET'
                           )


@twitter.tokengetter
def get_twitter_token(token=None):
    return flask_session.get('twitter_token')


@app.before_request
def before_request():
    shop_id = request.view_args.get('shop_id')
    product_id = request.view_args.get('product_id')
    g.shop = db_session.query(ComputerShop).filter_by(id=shop_id).first()
    g.product = db_session.query(Product).filter_by(id=product_id).first()
    g.username = flask_session.get('username')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.username is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def shop_owner_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        shop = db_session.query(ComputerShop).filter_by(id=g.shop.id).one()
        if shop.user.username != g.username:
            abort(401)
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
@app.route("/shops")
def home():
    shops = db_session.query(ComputerShop).all()
    return render_template('index.html', shops=shops)


@app.route("/shop/new", methods=["GET", "POST"])
@login_required
def create_shop():
    username = flask_session.get('username')
    user = db_session.query(User).filter_by(username=username).one()
    if request.method == 'POST':
        if request.form['name']:
            new_shop = ComputerShop(name=request.form['name'], user=user)
            db_session.add(new_shop)
            db_session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('shop-new.html')


@app.route("/shop/<int:shop_id>")
def get_shop(shop_id):
    shop = g.shop
    products = db_session.query(Product).filter_by(computer_shop_id=shop.id).all()
    return render_template('shop.html', shop=shop, products=products)


@app.route("/shop/<int:shop_id>/edit", methods=["GET", "POST"])
@login_required
@shop_owner_required
def edit_shop(shop_id):
    shop = g.shop
    if request.method == 'POST':
        if request.form['name']:
            shop.name = request.form['name']
            db_session.add(shop)
            db_session.commit()
        return redirect(url_for('get_shop', shop_id=shop.id))
    else:
        return render_template('shop-edit.html', shop=shop)


@app.route("/shop/<int:shop_id>/delete", methods=["GET", "POST"])
@login_required
@shop_owner_required
def delete_shop(shop_id):
    shop = g.shop
    if request.method == 'POST':
        db_session.delete(shop)
        db_session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('shop-delete.html', shop=shop)


@app.route("/shop/<int:shop_id>/product/new", methods=["GET", "POST"])
@login_required
@shop_owner_required
def create_product(shop_id):
    shop = g.shop
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
    shop = g.shop
    product = g.product
    return render_template('product.html', shop=shop, product=product)


@app.route("/shop/<int:shop_id>/product/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
@shop_owner_required
def edit_product(shop_id, product_id):
    shop = g.shop
    product = g.product
    if request.method == 'POST':
        product.name = request.form["name"]
        product.description = request.form["description"]
        product.price = request.form["price"]
        db_session.add(product)
        db_session.commit()
        return redirect(
            url_for('get_product', shop_id=shop.id, product_id=product.id))
    else:
        return render_template('product-edit.html', shop=shop, product=product)


@app.route("/shop/<int:shop_id>/product/<int:product_id>/delete", methods=["GET", "POST"])
@login_required
@shop_owner_required
def delete_product(shop_id, product_id):
    shop = g.shop
    product = g.product
    if request.method == 'POST':
        db_session.delete(product)
        db_session.commit()
        return redirect(url_for('get_shop', shop_id=shop.id))
    else:
        return render_template('product-delete.html', shop=shop, product=product)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['email']
        password = request.form['password']
        user = db_session.query(User).filter_by(username=username).first()
        if not user or not user.verify_password(password):
            return render_template('login.html', login_incorrect=True)
        else:
            flask_session['username'] = username
            return redirect(url_for('home'))
    else:
        if 'username' in flask_session:
            return redirect(url_for('home'))
        else:
            return render_template('login.html', login_incorrect=False)


@app.route('/twitter-login')
def twitter_login():
    return twitter.authorize(
        callback=url_for('oauth_authorized',
                         next=request.args.get('next') or request.referrer or None))


@app.route('/twitter-oauth-authorized')
def oauth_authorized():
    resp = twitter.authorized_response()
    if resp is None:
        return render_template('error.html', error_message='Failed to sign in with Twitter')

    twitter_username = resp['screen_name']
    user = db_session.query(User).filter_by(username=twitter_username).first()
    if not user:
        user = User(username=twitter_username)
        db_session.add(user)
        db_session.commit()

    flask_session['username'] = twitter_username
    flask_session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )

    return redirect(url_for('home'))


@app.route("/logout", methods=["GET", "POST"])
def logout():
    flask_session.pop('username', None)
    flask_session.pop('twitter_token', None)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.debug = True
    app.run(port=8080)
