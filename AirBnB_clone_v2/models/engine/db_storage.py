#!/usr/bin/python3
""" This module defines the DBStorage """


from os import getenv
import models
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """ Defines a new engine

    Private class attributes:
        __engine : SQLAlchemy engine.
        __session: SQLAlchemy session."""
    __engine = None
    __session = None

    def __init__(self):
        """Initializing DBStorage instances"""
        # Create the engine
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        # Drop all the tables if HBNB_ENV==test
        if getenv("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns dictionary with all objects depending
        of the class name (argument cls)"""
        if cls:
            objs = self.__session.query(self.classes()[cls])
        else:
            objs = self.__session.query(State).all()
            objs += self.__session.query(City).all()
            objs += self.__session.query(User).all()
            objs += self.__session.query(Place).all()
            objs += self.__session.query(Amenity).all()
            objs += self.__session.query(Review).all()

        dic = {}
        for obj in objs:
            k = '{}.{}'.format(type(obj).__name__, obj.id)
            dic[k] = obj
        return dic

    def new(self, obj):
        """Add the object to the current db session (self.__session)"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current db session (self.__session)"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current db session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database (feature of SQLAlchemy)
        Create the current database session (self.__session)
        from the engine (self.__engine) by using a sessionmaker
        """
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session
