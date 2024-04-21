#!/usr/bin/python3
""" State Module for HBNB project """
import sqlalchemy
from os import getenv
from models import storage
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base



class State(BaseModel, Base):
    """ State class """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'states'
        name = Column(
            String(128),
            nullable=False
        )
        cities = relationship(
            "City",
            cascade="all, delete",
            backref="states"
        )
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            """Returns the cities in this State"""
            cities_in_state = storage.all("City").values()
            cities_list = []
            for city in cities_in_state:
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
