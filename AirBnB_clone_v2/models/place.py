#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from os import getenv
from models.amenity import Amenity
from models.review import Review
import models

# Add an instance of SQLAlchemy Table called place_amenity
# for creating the relationship Many-To-Many between Place and Amenity:
place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    if getenv("HBNB_TYPE_STORAGE") == "db":
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float)
        longitude = Column(Float)

        # For DBStorage:
        # Class attribute reviews representing relationship with Review.
        reviews = relationship("Review", cascade="all, delete",
                               backref="place")
        # Class Attribute amenities representing relationship with Amenity
        # no need to backref=place_amenities:
        # the name exists on mapper 'Mapper|Amenity|amenities'
        amenities = relationship("Amenity", secondary='place_amenity',
                                 viewonly=False)

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

# for Filestorage:
        @property
        def reviews(self):
            """Getter for reviews
            Returns: list of Review instance with places.id=Place.id
            It will be FileStorage relashionship btwn Place and Review
            """
            new = []
            for element in models.storage.all(Review):
                if element.place_id == self.id:
                    new.append(element)
            return new

        @property
        def amenities(self):
            """Getter for amenities
            Returns: list of Amenity instances based on  amenity_ids that
            contains all Amenity.id linked to the Place"""
            new = []
            for element in models.storage.all(Amenity):
                if new.id in self.amenity_ids:
                    new.append(element)
            return new

        @amenities.setter
        def amenities(self, obj):
            """Setter for amenities Object
            Adds an Amenity.id to the attribute amenity_ids
            """
            if type(obj) == Amenity:
                self.amenity_ids.append(obj.id)
