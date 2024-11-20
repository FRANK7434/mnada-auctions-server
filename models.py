from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
import datetime

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class User(db.Model,SerializerMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime)
    role = db.Column(db.String(50), nullable=False)

    # Relationships
    items = db.relationship('Item', back_populates='user')
    bids=db.relationship("Bid",back_populates="user")
    notifications=db.relationship("Notification", back_populates='user')
    logs=db.relationship("AuditLog",back_populates='user')
   
    #serialise rules
    serialize_rules=('-items','-bids.user','-notifications.user','-logs','-password')

class Item(db.Model,SerializerMixin):
    __tablename__ = 'items'
    item_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    starting_price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    posted_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    auction_id=db.Column(db.Integer,db.ForeignKey("auctions.auction_id"),nullable=False)

    # Relationships
    user=db.relationship("User",back_populates='items')
    images=db.relationship("Image",back_populates='item')
    auction=db.relationship("Auction",back_populates='items')
    bid=db.relationship("Bid",back_populates='items')
    
    #serialise rules
    serialize_rules=('-user.items','-images.item','-auction.items','-bid.items')

class Image(db.Model,SerializerMixin):
    __tablename__ = 'images'
    image_id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(200), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'), nullable=False)
    #relationships
    item=db.relationship("Item",back_populates='images')

    #serialise rules
    serialize_rules=('-item',)


class Auction(db.Model,SerializerMixin):
    __tablename__ = 'auctions'
    auction_id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String,nullable=False)
    date=db.Column(db.String,nullable=False)
    start_time = db.Column(db.String, nullable=False)
    end_time = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)

    # Relationships
    items=db.relationship("Item",back_populates="auction")
    
    #serialise rules
    serialize_rules=('-items.auction',)

class Bid(db.Model,SerializerMixin):
    __tablename__ = 'bids'
    bid_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())
    bidder_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'), nullable=False)

    # Relationships
    user=db.relationship("User",back_populates="bids")
    items=db.relationship("Item",back_populates="bid")

    #serialise rules
    serialize_rules=('-user.bids','-items.bid')

# class BidHistory(db.Model,SerializerMixin):
#     __tablename__ = 'bid_histories'
#     history_id = db.Column(db.Integer, primary_key=True)
#     bid_id = db.Column(db.Integer, db.ForeignKey('bids.bid_id'), nullable=False)
#     auction_id = db.Column(db.Integer, db.ForeignKey('auctions.auction_id'), nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.datetime.now())


class Report(db.Model,SerializerMixin):
    __tablename__ = 'reports'
    report_id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(50), nullable=False)
    generated_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.datetime.now())

class AuditLog(db.Model,SerializerMixin):
    __tablename__ = 'audit_logs'
    log_id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    #relationships
    user=db.relationship("User",back_populates='logs')

    #serialise rules
    serialize_rules=('-user',)

class Notification(db.Model,SerializerMixin):
    __tablename__ = 'notifications'
    notification_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())

    #relationships
    user=db.relationship("User", back_populates='notifications')

    #serialise rules
    serialize_rules=('-user')
