from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
import datetime

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime)
    role = db.Column(db.String(50), nullable=False)

    # Relationships
    items = db.relationship('Item', back_populates='user')
    bids = db.relationship("Bid", back_populates="user")
    notifications = db.relationship("Notification", back_populates='user')
    logs = db.relationship("AuditLog", back_populates='user')

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "role": self.role,
        }

class Item(db.Model):
    __tablename__ = 'items'
    item_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    starting_price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    posted_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    auction_id = db.Column(db.Integer, db.ForeignKey("auctions.auction_id"), nullable=False)

    # Relationships
    user = db.relationship("User", back_populates='items')
    images = db.relationship("Image", back_populates='item')
    auction = db.relationship("Auction", back_populates='items')
    bid = db.relationship("Bid", back_populates='items')

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "title": self.title,
            "description": self.description,
            "starting_price": self.starting_price,
            "category": self.category,
            "posted_by": self.posted_by,
            "auction_id": self.auction_id,
        }

class Image(db.Model):
    __tablename__ = 'images'
    image_id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(200), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'), nullable=False)

    # Relationships
    item = db.relationship("Item", back_populates='images')

    def to_dict(self):
        return {
            "image_id": self.image_id,
            "image_url": self.image_url,
            "item_id": self.item_id,
        }

class Auction(db.Model):
    __tablename__ = 'auctions'
    auction_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    start_time = db.Column(db.String, nullable=False)
    end_time = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)

    # Relationships
    items = db.relationship("Item", back_populates="auction")

    def to_dict(self):
        return {
            "auction_id": self.auction_id,
            "name": self.name,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status": self.status,
        }

class Bid(db.Model):
    __tablename__ = 'bids'
    bid_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())
    bidder_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.item_id'), nullable=False)

    # Relationships
    user = db.relationship("User", back_populates="bids")
    items = db.relationship("Item", back_populates="bid")

    def to_dict(self):
        return {
            "bid_id": self.bid_id,
            "amount": self.amount,
            "timestamp": self.timestamp.isoformat(),
            "bidder_id": self.bidder_id,
            "item_id": self.item_id,
        }

class Report(db.Model):
    __tablename__ = 'reports'
    report_id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(50), nullable=False)
    generated_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def to_dict(self):
        return {
            "report_id": self.report_id,
            "report_type": self.report_type,
            "generated_by": self.generated_by,
            "generated_at": self.generated_at.isoformat(),
        }

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    log_id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    # Relationships
    user = db.relationship("User", back_populates='logs')

    def to_dict(self):
        return {
            "log_id": self.log_id,
            "action": self.action,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id,
        }

class Notification(db.Model):
    __tablename__ = 'notifications'
    notification_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now())

    # Relationships
    user = db.relationship("User", back_populates='notifications')

    def to_dict(self):
        return {
            "notification_id": self.notification_id,
            "message": self.message,
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat(),
        }
