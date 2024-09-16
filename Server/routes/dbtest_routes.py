from flask import Blueprint, request, jsonify , make_response
from sqlalchemy.exc import SQLAlchemyError

from utils.tokenutils import token_required , authorize , is_authorized_to_create , is_authorized_to_modify
from utils.server_responseutils import item_not_found_response , server_error_response , bad_request_response , unauthorized_response
from utils.constants import ALLOWED_ATTRIBUTES
from repo.card_in_deck_repo import CardinDeckRepository
from repo.user_repo import UserRepository
from repo.card_repo import CardRepository
from repo.cardinSet_repo import CardinSetRepository
from repo.deck_repo import DeckRepository
from repo.inventory_repo import InventoryRepository
from repo.Releasesets_repo import ReleaseSetsRepository

from models import Card , CardinDeck , Deck
from config import db

test_bp = Blueprint('test' , __name__)

@test_bp.route('/getUser/<int:id>')
def getUser(id):
    repo = UserRepository()
    data = repo.get_item_by_id(id)
    response = make_response(data.to_dict())
    return response

@test_bp.route('/getCard/<int:id>')
def getCard(id):
    repo = CardRepository()
    data = repo.get_item_by_id(id)
    response = make_response(data.to_dict())
    return response

@test_bp.route('/getCardinSet/<int:id>')
def getCardinSet(id):
    repo = CardinSetRepository()
    data = repo.get_item_by_id(id)
    response = make_response(data.to_dict())
    return response

@test_bp.route('/getDeck/<int:id>')
def getDeck(id):
    repo = DeckRepository()
    data = repo.get_item_by_id(id)
    response = make_response(data.to_dict())
    return response

@test_bp.route('/getInventory/<int:id>')
def getInventory(id):
    repo = InventoryRepository()
    data = repo.get_item_by_id(id)
    response = make_response(data.to_dict())
    return response

@test_bp.route('/getReleaseSet/<int:id>')
def getReleaseSet(id):
    repo = ReleaseSetsRepository()
    data = repo.get_item_by_id(id)
    response = make_response(data.to_dict())
    return response