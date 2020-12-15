from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    city = Column(String(64))

    def as_json(self):
        return {'id': self.id, 'name': self.city}


class EventType(Base):
    __tablename__ = 'event_types'

    id = Column(Integer, primary_key=True)
    event_type = Column(String(32))

    def as_json(self):
        return {'id': self.id, 'name': self.event_type}


class EventCategory(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    category = Column(String(64))

    def as_json(self):
        return {'id': self.id, 'name': self.category}


class EventCategoryLink(Base):
    __tablename__ = 'event_category_links'

    event_id = Column(Integer,
                      ForeignKey('events.id'),
                      primary_key=True)
    event = relationship('Event')

    category_id = Column(Integer,
                         ForeignKey('categories.id'),
                         primary_key=True)
    category = relationship('EventCategory')

    def __init__(self, category=None, event=None):
        self.category = category
        self.event = event


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    event_time = Column(DateTime(timezone=True))
    place = Column(String(256))
    source_url = Column(String(256))
    description = Column(Text)
    logo_path = Column(String(256))

    city_id = Column('city', Integer,
                     ForeignKey('cities.id'),
                     nullable=False, default=1)
    city = relationship('City', backref='events')

    event_type_id = Column('event_type', Integer,
                           ForeignKey('event_types.id'),
                           nullable=False, default=1)
    event_type = relationship('EventType', backref='events')

    event_category_links = relationship('EventCategoryLink',
                                        lazy='dynamic')
    categories = association_proxy('event_category_links', 'category')

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'event_time': self.event_time.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'place': self.place,
            'source_url': self.source_url,
            'description': self.description,
            'logo_path': self.logo_path,
            'city': self.city.as_json(),
            'event_type': self.event_type.as_json(),
            'categories': [
                category.as_json() for category in self.categories
            ]
        }
