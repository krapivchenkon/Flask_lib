import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email,
        }


# class MenuItem(Base):
#     __tablename__ = 'menu_item'

#     name = Column(String(80), nullable=False)
#     id = Column(Integer, primary_key=True)
#     description = Column(String(250))
#     price = Column(String(8))
#     course = Column(String(250))
#     user_id = Column(Integer, ForeignKey('user.id'))
#     user = relationship(Restaurant)

#     @property
#     def serialize(self):
#         """Return object data in easily serializeable format"""
#         return {
#             'name': self.name,
#             'description': self.description,
#             'id': self.id,
#             'price': self.price,
#             'course': self.course,
#         }


def init_db(session):
    user1 = User(name="User1",email="user1@gmail.com")

    session.add(user1)
    session.commit()

    user2 = User(name="User2",email="user2@example.com")
 
    session.add(user2)
    session.commit()

    user3 = User(name="User Test",email="user3_test@gmail.com")

    session.add(user3)
    session.commit()


if __name__ == '__main__':

    engine = create_engine('sqlite:///test_user.db')
    Base.metadata.create_all(engine)

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    init_db(session)
