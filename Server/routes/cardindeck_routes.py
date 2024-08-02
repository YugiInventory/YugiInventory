from flask import Blueprint, request, jsonify , make_response

from utils.tokenutils import token_required

cardinDeck_bp = Blueprint('cardinDeck' , __name__)

@cardinDeck_bp.route('/addCardtoDeck' , methods=["POST"])
@token_required
def add_card_to_deck(user_id):
    pass

@cardinDeck_bp.route('/editCardinDeck' , methods=["PATCH"])
@token_required
def edit_card_in_deck(user_id):
    pass

@cardinDeck_bp.route('/deleteCardinDeck', methods=["POST"])
@token_required
def delete_card_in_deck(user_id):
    pass