from database import db

class EventCategory(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64))

class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(64))

class UserStatus(db.Model):
    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(32))

class UserStack(db.Model):
    __tablename__ = 'stacks'

    id = db.Column(db.Integer, primary_key=True)
    stack = db.Column(db.String(64))

class EventType(db.Model):
    __tablename__ = 'event_types'

    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(32))

favorites_table = db.Table('favorites',
    db.Column('user_id', db.Integer,
              db.ForeignKey('users.id'),
              primary_key=True),
    db.Column('event_id', db.Integer,
              db.ForeignKey('events.id'),
              primary_key=True)
)

user_stack_links_table = db.Table('user_stack_links',
    db.Column('user_id', db.Integer,
              db.ForeignKey('users.id'),
              primary_key=True),
    db.Column('stack_id', db.Integer,
              db.ForeignKey('stacks.id'),
              primary_key=True)
)

event_category_links_table = db.Table('event_category_links',
    db.Column('event_id', db.Integer,
              db.ForeignKey('events.id'),
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

    categories = db.relationship('EventCategory',
                                 lazy='subquery',
                                 secondary=event_category_links_table,
                                 backref=db.backref('events', lazy=True))

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

    favorites = db.relationship('Event',
                                secondary=favorites_table,
                                lazy='subquery')

    stack = db.relationship('UserStack',
                            secondary=user_stack_links_table,
                            lazy='subquery')
