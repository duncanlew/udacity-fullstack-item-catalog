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

computer_shop_1 = ComputerShop(name="Si Computers", user=user)
computer_shop_2 = ComputerShop(name="Super Duper Tech Shop", user=user)

session.add(user)
session.commit()

session.add(computer_shop_1)
session.commit()

session.add(computer_shop_2)
session.commit()

session.commit()
