from email.policy import default
from enum import unique
from sys import settrace
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import ForeignKey
from market import db 
from market import admin
from sqlalchemy.ext.declarative import declarative_base
from market import bcrypt
from market import login_manager
from flask_login import UserMixin
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False,unique=True)
    budget = db.Column(db.Float(),nullable=False,default=1000.00)
    password_hash = db.Column(db.String(length=60),nullable=False)
    items = db.relationship('item',backref='owned_user',lazy=True)

    @property
    def password(self):
        return self.password
    @password.setter
    def password(self,plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def __repr__(self):
        return f'{self.username}'

class item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)
    price = db.Column(db.Float(),nullable=False)
    barcode = db.Column(db.String(length=12),nullable=False,unique=True)
    description = db.Column(db.String(length=1024),nullable=True,unique=True)
    owner = db.Column(db.Integer(),db.ForeignKey('user.id'))
    def __repr__(self):
        return f'{self.name}'
        
    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()