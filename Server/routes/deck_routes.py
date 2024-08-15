from flask import Blueprint, make_response , jsonify , request
from sqlalchemy.exc import SQLAlchemyError

#local imports
from utils.tokenutils import token_required , authorize , is_authorized_to_modify , is_authorized_to_create
from utils.server_responseutils import server_error_response , bad_request_response , item_not_found_response
from utils.constants import ALLOWED_ATTRIBUTES
from repo.deck_repo import DeckRepository
from config import db
from models import Deck , CardinDeck

from pprint import pprint

deck_bp = Blueprint('deck',__name__)

@deck_bp.route('/createSingleDeck', methods=["POST"])
@token_required
@authorize(is_authorized_to_create,edit=False)
def create_single_deck(user_id,**kwargs):
    
    data = request.get_json()

    try:
        name = data["name"]
    except:
        response = make_response({},400)
        return response

    repo = DeckRepository()
    result = repo.create(user_id=user_id, name=name)
    print(result)
    if result.status == True:
        print('I think i see the issue')
        try:
            db.session.commit()
            response = make_response({'Success':'Deck created'},201)
        except Exception as e:
            #Figure out what the Error Class maybe
            #Depending on the Error Class figure out which function to run
            #That function will return 
            print(e)
            print(type(e))
            pprint(vars(e))
            pprint('fff')
            response = make_response({},400)

    else:
        #Figure out what the Error Class maybe
        #Depending on the Error Class figure out which function to run
        #That function will return 

        error_obj = result.return_data
        pprint(vars(error_obj))
        print(type(error_obj))
        response = server_error_response()

    return response

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
@authorize(is_authorized_to_modify, edit=True)
def edit_single_deck(user_id,**kwargs):
    users_deck = kwargs['resource']
    try:
        for key,value in kwargs.items():  #only allow select keys to be modified as well
            if hasattr(users_deck,key) and key in ALLOWED_ATTRIBUTES["Deck"]:
                setattr(users_deck,key,value)
        db.session.add(users_deck)
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
    return response

@deck_bp.route('/deleteSingleDeck', methods=['POST'])
@token_required
@authorize(is_authorized_to_modify, edit=True)
def delete_single_deck(user_id,**kwargs):
    deck_to_delete = kwargs["resource_id"]
    
    #needs to delete all the cards in that deck as well. 
    
    #Replaced with CardinDeck access function
    cards_in_deck = CardinDeck.query.filter(CardinDeck.deck_id==deck_to_delete.id).all() 

    try:
        for single_card in cards_in_deck:
            db.session.delete(single_card)
        db.session.delete(deck_to_delete)
        db.session.commit()
        response = make_response({},204)
    except SQLAlchemyError as se:
        db.session.rollback()
        print(se)
        response = server_error_response()
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
def get_single_deck_card_info(deck_id):

    #Replace with access functions 
    single_deck = Deck.query.filter(Deck.id==deck_id).first()
    if single_deck:
        try:
            response = make_response(jsonify(single_deck.to_dict()),200)
        except SQLAlchemyError as se:
            print(se)
            response = server_error_response()
    else:
        response = item_not_found_response()
    return response
