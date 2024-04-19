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
    __tablename__ = 'states'
    name = Column(
        String(128), nullable=False
    ) if getenv('HBNB_TYPE_STORAGE') == 'db' else ''
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship(
            'City',
            cascade='all, delete',
            backref='state'
        )
    else:
        @property
        def cities(self):
            """Returns the cities in this State"""
            cities_state = []
            for v in storage.all("City").values():
                if v.state_id == self.id:
                    cities_state.append(v)
            return cities_state
