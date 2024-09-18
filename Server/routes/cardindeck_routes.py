from flask import Blueprint, request, jsonify , make_response
from sqlalchemy.exc import SQLAlchemyError

from utils.tokenutils import token_required , authorize , is_authorized_to_create , is_authorized_to_modify
from utils.server_responseutils import item_not_found_response , server_error_response , bad_request_response , unauthorized_response
from utils.constants import ALLOWED_ATTRIBUTES
from repo.card_in_deck_repo import CardinDeckRepository
from repo.card_repo import CardRepository

from models import Card , CardinDeck , Deck
from config import db

cardinDeck_bp = Blueprint('cardinDeck' , __name__)

@cardinDeck_bp.route('/addCardtoDeck' , methods=["POST"])
@token_required
@authorize(is_authorized_to_create,edit=False)
def add_card_to_deck(user_id,**kwargs):
    print(kwargs)
    print(user_id)

    try:
        #Get the card, then get then check if that card exists in the deck also
        card_repo = CardRepository()
        card_to_add = card_repo.get_item_by_id(kwargs["resource_id"])
        if card_to_add:
            #find the cardindeck item location/card_id
            cardindeck_repo = CardinDeckRepository()
            filters = []
            for key, value in kwargs.items():
                if key in CardinDeckRepository.card_filters:
                    filters.append(CardinDeckRepository.card_filters[key](value))           
            isduplicate = cardindeck_repo.filter(*filters).first()
            if isduplicate:
                print('icecream?')
                new_card_quantity = int(isduplicate.quantity) + int(kwargs['quantity'])
                print(f'The new card quantity is {new_card_quantity}' )
                updated_card = cardindeck_repo.update_and_commit({"quantity":new_card_quantity},isduplicate)
                response = make_response({"Duplicate Found":"Combined Quantity"}, 250)
            else:
                print(kwargs["quantity"])
                new_card = cardindeck_repo.create_and_commit(kwargs["resource_id"],kwargs["deck_id"],kwargs["location"],kwargs["quantity"])
                response = make_response(jsonify(new_card.to_dict()),201)
        else:
            response = item_not_found_response()
        return response
    except SQLAlchemyError as se:
        print(se)
        response = server_error_response()
    except ValueError as ve:
        print(ve)
        print('we have a value error')
        response = bad_request_response()
    except Exception as e:
        print(e)
        print('hahgfsgfsgaxd')
        response = server_error_response()
    return response
    


@cardinDeck_bp.route('/editCardinDeck' , methods=["PATCH"])
@token_required
@authorize(is_authorized_to_modify, edit=True)
def edit_card_in_deck(user_id,**kwargs):
    try:
        users_card_in_deck = kwargs["resource"]
        repo = CardinDeckRepository()
        updated_card = repo.update_and_commit(params_dict=kwargs, resource=users_card_in_deck)
        response = make_response({},202)
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
    try:
        card_to_delete = kwargs["resource"]
        # card_to_delete = CardinDeck.query.filter(CardinDeck.id==resource_id).first()
        repo = CardinDeckRepository()
        repo.delete_and_commit(resource=card_to_delete)
        response = make_response({},204)
    except SQLAlchemyError as se:   
        print(se)
        db.session.rollback()
        response = server_error_response()
    return response 

@cardinDeck_bp.route('/moveCardinDeck', methods=["POST"])
@token_required
@authorize(is_authorized_to_modify, edit=True)
def move_card_in_deck(user_id,**kwargs):
    #When moving a card you are reducing the value of 1 card and then creating a new card
    #reducing the value can either be to 0 which is delete, or modify the value. 
    #This might be needed to make sure the movemment of a card can all be done in 1 transaction
    #removed the 
    pass    