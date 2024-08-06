from flask import Blueprint, request, jsonify , make_response
from sqlalchemy.exc import SQLAlchemyError

from utils.tokenutils import token_required , authorize , is_authorized_to_create , is_authorized_to_modify
from utils.server_responseutils import item_not_found_response , server_error_response , bad_request_response , unauthorized_response

from models import Card , CardinDeck , Deck
from config import db

cardinDeck_bp = Blueprint('cardinDeck' , __name__)

@cardinDeck_bp.route('/addCardtoDeck' , methods=["POST"])
@token_required
@authorize(is_authorized_to_create)
def add_card_to_deck(**kwargs):
    data = request.get_json()
    
    card_to_add = Card.query.filter(Card.id==data['card_id']).first()
    print('lala')
    
    if card_to_add:
        try:
            new_card_in_deck = CardinDeck(
                quantity = data['quantity'],
                location = data['location'],
                deck_id = data['deck_id'],
                card_id = card_to_add.id
            )
            db.session.add(new_card_in_deck)
            db.session.commit()
            response = make_response({"Sucess":"Card Added"},201)
        except SQLAlchemyError as se:
            print(se)
            db.session.rollback()
            response = server_error_response()
        except ValueError as ve:
            print(ve)
            db.session.rollback()
            response = bad_request_response()
    else:
        response = item_not_found_response()

    return response


@cardinDeck_bp.route('/editCardinDeck' , methods=["PATCH"])
@token_required
@authorize(is_authorized_to_modify)
def edit_card_in_deck(**kwargs):
    resource_id = kwargs["resource_id"]

    card_to_modify = CardinDeck.query.filter(CardinDeck.id==resource_id).first()

    if card_to_modify:
        try:
            for key,value in kwargs.items():
                if hasattr(card_to_modify,key):
                    setattr(card_to_modify,key,value)
            db.session.add(card_to_modify)
            db.session.commit()
            response = make_response({},200)
        except SQLAlchemyError as se:
            print(se)
            db.session.rollback()
            response = server_error_response()
        except ValueError as ve:
            print(ve)
            response = bad_request_response()
    else:
        response = item_not_found_response()
    return response

@cardinDeck_bp.route('/deleteCardinDeck', methods=["POST"])
@token_required
@authorize(is_authorized_to_modify)
def delete_card_in_deck(**kwargs):
    resource_id = kwargs["resource_id"]
    card_to_delete = CardinDeck.query.filter(CardinDeck.id==resource_id).first()

    if card_to_delete:
        try:
            db.session.delete(card_to_delete)
            db.session.commit()
            response = make_response({},204)
        except SQLAlchemyError as se:   
            print(se)
            db.session.rollback()
            response = server_error_response()
    else:
        response = item_not_found_response()
    return response 