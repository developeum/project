from .database import db, association_proxy

class EventCategory(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64))

    def as_json(self):
        return {'id': self.id, 'name': self.category}

class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(64))

    def as_json(self):
        return {'id': self.id, 'name': self.city}

class UserStatus(db.Model):
    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(32))

    def as_json(self):
        return {'id': self.id, 'name': self.status}

class EventType(db.Model):
    __tablename__ = 'event_types'

    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(32))

    def as_json(self):
        return {'id': self.id, 'name': self.event_type}

class UserVisit(db.Model):
    __tablename__ = 'user_visit_links'

    visit_time = db.Column(db.DateTime)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        primary_key=True)
    user = db.relationship('User')

    event_id = db.Column(db.Integer,
                         db.ForeignKey('events.id'),
                         primary_key=True)
    event = db.relationship('Event')

    def __init__(self, event=None, user=None, visit_time=None):
        self.event = event
        self.user = user
        self.visit_time = visit_time

class EventCategoryLink(db.Model):
    __tablename__ = 'event_category_links'

    event_id = db.Column(db.Integer,
                         db.ForeignKey('events.id'),
                         primary_key=True)
    event = db.relationship('Event')

    category_id = db.Column(db.Integer,
                            db.ForeignKey('categories.id'),
                            primary_key=True)
    category = db.relationship('EventCategory')

    def __init__(self, category=None, event=None):
        self.category = category
        self.event = event

user_stack_links_table = db.Table('user_stack_links',
    db.Column('user_id', db.Integer,
              db.ForeignKey('users.id'),
              primary_key=True),
    db.Column('category_id', db.Integer,
              db.ForeignKey('categories.id'),
              primary_key=True)
)

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    event_time = db.Column(db.DateTime(timezone=True))
    place = db.Column(db.String(256))
    source_url = db.Column(db.String(256))
    description = db.Column(db.Text)
    logo_path = db.Column(db.String(256))

    city_id = db.Column('city', db.Integer,
                        db.ForeignKey('cities.id'),
                        nullable=False, default=1)
    city = db.relationship('City', backref='events')

    event_type_id = db.Column('event_type', db.Integer,
                              db.ForeignKey('event_types.id'),
                              nullable=False, default=1)
    event_type = db.relationship('EventType', backref='events')

    event_category_links = db.relationship('EventCategoryLink',
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

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64))
    password = db.Column(db.String(60))
    phone = db.Column(db.String(24))
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    profile_img = db.Column(db.String(256))

    city_id = db.Column('city', db.Integer,
                        db.ForeignKey('cities.id'),
                        nullable=False, default=1)
    city = db.relationship('City')

    status_id = db.Column('status', db.Integer,
                          db.ForeignKey('statuses.id'),
                          nullable=False, default=1)
    status = db.relationship('UserStatus')

    user_visit = db.relationship('UserVisit',
                                 order_by='desc(UserVisit.visit_time)',
                                 lazy='dynamic')
    visited = association_proxy('user_visit', 'event')

    stack = db.relationship('EventCategory',
                            secondary=user_stack_links_table,
                            lazy='subquery')

    def as_json(self):
        return {
            'email': self.email,
            'phone': self.phone,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'profile_img': self.profile_img,
            'city': self.city.as_json(),
            'status': self.status.as_json(),
            'stack': [
                category.as_json() for category in self.stack
            ]
        }
