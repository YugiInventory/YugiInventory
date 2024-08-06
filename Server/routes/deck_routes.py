from flask import Blueprint, make_response , jsonify , request
from sqlalchemy.exc import SQLAlchemyError

#local imports
from utils.tokenutils import token_required , authorize , is_authorized_to_modify , is_authorized_to_create
from utils.server_responseutils import server_error_response , bad_request_response , item_not_found_response
from config import db
from models import Deck , CardinDeck

deck_bp = Blueprint('deck',__name__)

@deck_bp.route('/createSingleDeck', methods=["POST"])
@token_required
def create_single_deck(user_id, **kwargs):
    data = request.get_json()
    print(kwargs)
    user_id_test = kwargs.get("test")
    print(user_id)
    print(user_id_test)

    try:
        new_deck = Deck(
            isPublic = True,
            user_id = user_id,
            name = data['name']
        )

        db.session.add(new_deck)
        db.session.commit()
        response = make_response({'Sucess':'Deck Created'}, 201)
    except SQLAlchemyError as se:
        db.session.rollback()
        print(se)
        response = server_error_response()
    except ValueError as ve:
        db.session.rollback()
        print(ve)
        response = bad_request_response()
    
    return response

@deck_bp.route('/editSingleDeck', methods=["PATCH"])
@token_required
@authorize(is_authorized_to_modify)
def edit_single_deck(**kwargs):


    #Try to extract the arguements
    try:    
        deck_id = kwargs["resource_id"]
    except:
        response = bad_request_response()
        return response

    users_single_deck = Deck.query.filter(Deck.id==deck_id).first()

    if users_single_deck:
        try:
            for key,value in kwargs.items():  #data.items()
                if hasattr(users_single_deck,key):
                    setattr(users_single_deck,key,value)
            db.session.add(users_single_deck)
            db.session.commit()
            response = make_response({"Sucess":"Updated"},202)
        except ValueError as ve:
            print(ve)
            db.session.rollback()
            response = bad_request_response()
        except SQLAlchemyError as se:
            print(se)
            db.session.rollback()
            response = server_error_response()
    else:
        response = item_not_found_response()
    return response

@deck_bp.route('/deleteSingleDeck', methods=['POST'])
@token_required
@authorize(is_authorized_to_modify)
def delete_single_deck(**kwargs):

    try:
        deck_id = kwargs["resource_id"]
    except:
        response = bad_request_response()
        return response
    
    #needs to delete all the cards in that deck as well. 
    users_single_deck = Deck.query.filter(Deck.id==deck_id).first()
    
    if users_single_deck:
        cards_in_deck = CardinDeck.query.filter(CardinDeck.deck_id==users_single_deck.id).all() 
        try:
            for single_card in cards_in_deck:
                db.session.delete(single_card)
            db.session.delete(users_single_deck)
            db.session.commit()
            response = make_response({},204)
        except SQLAlchemyError as se:
            db.session.rollback()
            print(se)
            response = server_error_response()
    else:
        response = item_not_found_response()
    return response

@deck_bp.route('/getUsersDecks' , methods=["GET"])
@token_required
def get_users_decks(user_id):
    filter_mapping = {
        'user_id' : lambda value: Deck.user_id==value,
        'name' : lambda value: Deck.name.ilike(f'%{value}%'),
        'id' : lambda value: Deck.id==value
    }
    try:
        filter_elements = []
        for key,value in request.args.items():
            filter_element = filter_mapping[key](value)
            filter_elements.append(filter_element)
        deck_lists = Deck.query.filter(*filter_elements).all()
        deck_list = [deck.to_dict(rules=('-card_in_deck','-user')) for deck in deck_lists]
        response = make_response(jsonify(deck_list),200)
    except SQLAlchemyError as se:
        db.session.rollback()
        print(se)
        response = server_error_response()
    except KeyError as ke:
        print(ke)
        db.session.rollback()
        response = bad_request_response()
    return response

@deck_bp.route('/getSingleDeckCardInfo/<int:deck_id>', methods =['GET'])
def get_single_deck_card_info():
    pass

