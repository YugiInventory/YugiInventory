from flask import Blueprint, make_response , jsonify , request
from sqlalchemy.exc import SQLAlchemyError

#local imports
from utils.tokenutils import token_required
from utils.server_responseutils import server_error_response , bad_request_response
from config import db

deck_bp = Blueprint('deck',__name__)

@deck_bp.route('/createSingleDeck', methods=["POST"])
@token_required
def create_single_deck(user_id):
    data = request.get_json()

    try:
        new_deck = deck_bp(
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
def edit_single_deck(user_id):
    pass

@deck_bp.route('/deleteSingleDeck', methods=['POST'])
@token_required
def delete_single_deck(user_id):
    pass

@deck_bp.route('/getSingleDeckCardInfo/<int:deck_id>', methods =['GET'])
def get_single_deck_card_info():
    pass

