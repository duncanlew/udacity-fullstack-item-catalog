from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_model import Base, User, ComputerShop, Product

engine = create_engine('sqlite:///computer_shop.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
DBSession = sessionmaker(bind=engine)
session = DBSession()

user = User('admin', 'admin')

computer_shop_1 = ComputerShop(name="Fruity Tech Store", user=user)
computer_shop_2 = ComputerShop(name="Super Duper Tech Shop", user=user)
computer_shop_3 = ComputerShop(name="Android Phone Shop", user=user)

session.add(user)
session.commit()

session.add(computer_shop_1)
session.commit()

session.add(computer_shop_2)
session.commit()

session.add(computer_shop_3)
session.commit()

# Products of computer shop 1
product_1 = Product(name="MacBook Pro 2019", description="Excellent choice as a portable computer", price="1599.99",
                    computer_shop=computer_shop_1)
product_2 = Product(name="MacBook Pro 2018", description="Excellent choice as a portable computer", price="1499.99",
                    computer_shop=computer_shop_1)
product_3 = Product(name="MacBook Pro 2017", description="Excellent choice as a portable computer", price="1399.99",
                    computer_shop=computer_shop_1)
product_4 = Product(name="MacBook Pro 2016", description="Excellent choice as a portable computer", price="1299.99",
                    computer_shop=computer_shop_1)
product_5 = Product(name="MacBook Pro 2015", description="Excellent choice as a portable computer", price="1199.99",
                    computer_shop=computer_shop_1)
product_6 = Product(name="MacBook Pro 2014", description="Excellent choice as a portable computer", price="1099.99",
                    computer_shop=computer_shop_1)

# Products of computer shop 2
product_7 = Product(name="Logitech Keyboard", description="Keyboard with a lot of bang for your buck", price="88.99",
                    computer_shop=computer_shop_2)
product_8 = Product(name="MX awesome mouse", description="Highly revered by the tech community", price="55.99",
                    computer_shop=computer_shop_2)
product_9 = Product(name="Silent keyboard", description="Keyboard that does not make a sound while typing",
                    price="120.99", computer_shop=computer_shop_2)
product_10 = Product(name="Mechanical keyboard", description="Click feeling of typing made prominent", price="129.99",
                     computer_shop=computer_shop_2)
product_11 = Product(name="4000 dpi mouse", description="Very high precision mouse", price="99.99",
                     computer_shop=computer_shop_2)
product_12 = Product(name="Fashionable laptop case", description="Laptop case that is all the rage at the moment",
                     price="22.99", computer_shop=computer_shop_2)

# Products of computer shop 3
product_13 = Product(name="Samsung Galaxy S9", description="Excellent 9th generation of Samsung phones", price="799.99",
                     computer_shop=computer_shop_3)
product_14 = Product(name="Samsung Galaxy S10", description="Excellent 10th generation of Samsung phones",
                     price="899.99",
                     computer_shop=computer_shop_3)
product_15 = Product(name="Samsung Note 10", description="Best 10th generation for note taking on a phone",
                     price="999.99", computer_shop=computer_shop_3)
product_16 = Product(name="Samsung Note 10+", description="Note taking on a bigger screen!", price="1099.99",
                     computer_shop=computer_shop_3)
product_17 = Product(name="Samsung Galaxy A10", description="Mid range for an affordable price", price="499.99",
                     computer_shop=computer_shop_3)
product_18 = Product(name="Samsung Galaxy A20", description="Mid range phone for those who needs more power",
                     price="599.99", computer_shop=computer_shop_3)

session.add(product_1)
session.commit()

session.add(product_2)
session.commit()

session.add(product_3)
session.commit()

session.add(product_4)
session.commit()

session.add(product_5)
session.commit()

session.add(product_6)
session.commit()

session.add(product_7)
session.commit()

session.add(product_8)
session.commit()

session.add(product_9)
session.commit()

session.add(product_10)
session.commit()

session.add(product_11)
session.commit()

session.add(product_12)
session.commit()

session.add(product_13)
session.commit()

session.add(product_14)
session.commit()

session.add(product_15)
session.commit()

session.add(product_16)
session.commit()

session.add(product_17)
session.commit()

session.add(product_18)
session.commit()
