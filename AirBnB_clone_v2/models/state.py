#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
import models

class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state', cascade='delete')

    if getenv("HBNB_TYPE_STORAGE") != 'db':
        @property
        def cities(self):
            """Gets the list of City instances with state_id=State.id"""
            city_list = []
            for city in list(models.storage.all(City)):
                if city.state_id == self.id:
                    city_list.append(city)
                    return city_list
