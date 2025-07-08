from app import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask import Flask, render_template, request


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    scans = db.relationship('Scan')

    def __repr__(self):
        return f'<User {self.username}>'

class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scanName = db.Column(db.String(150), unique=True, nullable=False)
    ipaddress = db.Column(db.String(150), nullable=False)
    domain = db.Column(db.String(150), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Scan {self.scanName}>'