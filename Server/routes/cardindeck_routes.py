from flask import Blueprint, request, jsonify , make_response
from sqlalchemy.exc import SQLAlchemyError

from utils.tokenutils import token_required , authorize , is_authorized_to_create , is_authorized_to_modify
from utils.server_responseutils import item_not_found_response , server_error_response , bad_request_response , unauthorized_response
from utils.constants import ALLOWED_ATTRIBUTES

from models import Card , CardinDeck , Deck
from config import db

cardinDeck_bp = Blueprint('cardinDeck' , __name__)

@cardinDeck_bp.route('/addCardtoDeck' , methods=["POST"])
@token_required
@authorize(is_authorized_to_create,edit=False)
def add_card_to_deck(user_id,**kwargs):
    #Check to see if location matches for table
    #Try to extract needed parameters

    try:
        resource_id = kwargs["resource_id"]
        deck_id = kwargs["deck_id"]
        location = kwargs["location"]
        quantity = kwargs["quantity"]
    except:
        response = bad_request_response()
        return response

    card_to_add = Card.query.filter(Card.id==resource_id).first()
    
    if card_to_add:
        #need to check for duplicate

        isduplicate = CardinDeck.query.filter(CardinDeck.card_id==resource_id,CardinDeck.location==location,CardinDeck.deck_id==deck_id).first()

        if isduplicate:
            try:
                new_card_quantity = int(isduplicate.quantity) + int(quantity)
                isduplicate.quantity = new_card_quantity
                db.session.add(isduplicate)
                db.session.commit()
                response = make_response({"Duplicate Entry":"Combined Total Quantity"},250)
            except SQLAlchemyError as se:
                print(se)
                db.session.rollback()
                response = server_error_response()
            except ValueError as ve:
                print(ve)
                db.session.rollback()
                response = bad_request_response()
        else:
            try:
                new_card_in_deck = CardinDeck(
                    quantity = quantity,
                    location = location,
                    deck_id = deck_id,
                    card_id = resource_id
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
@authorize(is_authorized_to_modify, edit=True)
def edit_card_in_deck(user_id,**kwargs):
    users_card_in_deck = kwargs["resource"]

    # card_to_modify = CardinDeck.query.filter(CardinDeck.id==resource_id).first()

    try:
        for key,value in kwargs.items():
            if hasattr(users_card_in_deck,key) and key in ALLOWED_ATTRIBUTES["CardinDeck"]:
                setattr(users_card_in_deck,key,value)
        db.session.add(users_card_in_deck)
        db.session.commit()
        response = make_response({},200)
    except SQLAlchemyError as se:
        print(se)
        db.session.rollback()
        response = server_error_response()
    except ValueError as ve:
        print(ve)
        response = bad_request_response()
    return response

@cardinDeck_bp.route('/deleteCardinDeck', methods=["POST"])
@token_required
@authorize(is_authorized_to_modify, edit=True)
def delete_card_in_deck(user_id,**kwargs):
    resource_id = kwargs["resource_id"]
    card_to_delete = kwargs["resource"]
    # card_to_delete = CardinDeck.query.filter(CardinDeck.id==resource_id).first()

    try:
        db.session.delete(card_to_delete)
        db.session.commit()
        response = make_response({},204)
    except SQLAlchemyError as se:   
        print(se)
        db.session.rollback()
        response = server_error_response()
    return response 