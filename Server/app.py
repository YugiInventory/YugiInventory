#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from models import *
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request, session
import os

# Local imports

from config import app, db
from models import User, Card, Deck, CardinSet, Banlist, BanlistCard


@app.route('/')
def home():
    return 'test'

@app.route('/users')
def users():
    userinfo = db.session.query(User).all()
    user_list = []
    for user in userinfo:
        user_list.append(user.to_dict())
    
    response = make_response(jsonify(user_list),200)
    return response





if __name__ == '__main__':

    app.run(port=5555, debug=True)
