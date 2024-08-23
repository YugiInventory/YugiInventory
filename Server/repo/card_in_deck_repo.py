from .repository_interface import ReadWriteRepositoryInterface
from utils.constants import ALLOWED_ATTRIBUTES
from models import CardinDeck
from flask_sqlalchemy import SQLAlchemy
from config import db
from sqlalchemy.exc import SQLAlchemyError

class CardinDeckRepository(ReadWriteRepositoryInterface):
    card_filters = {
        'card_id' : lambda value: CardinDeck.card_id==value,
        'location' : lambda value: CardinDeck.location==value,
        'deck_id' : lambda value: CardinDeck.deck_id==value,
    }
    
    def __init__(self):
        super().__init__(CardinDeck)
    
    def create(self, card_id, deck_id, location, quantity):
        new_CardinDeck = CardinDeck(
            quantity = quantity,
            location = location,
            deck_id = deck_id,
            card_id = card_id
        )
        db.session.commit(new_CardinDeck)
        return new_CardinDeck

    def create_and_commit(self, card_id, deck_id, location, quantity):
        new_cardinDeck = self.create(card_id,deck_id,location,quantity)
        db.session.commit()
        return new_cardinDeck

    # def update(self, params_dict, cardinDeck = None):
    #     if cardinDeck is None:
    #         try:
    #             cardinDeck = self.get_item_by_id(params_dict["resource_id"])
    #         except SQLAlchemyError as se:
    #             print(se)
    #     for key,value in params_dict.items():
    #         if hasattr(cardinDeck,key) and key in ALLOWED_ATTRIBUTES['CardinDeck']:
    #             setattr(cardinDeck,key,value)
    #     db.session.add(cardinDeck)
    #     return cardinDeck

    # def update_and_commit(self, params_dict, cardinDeck=None):
    #     updated_cardinDeck = self.update(params_dict,cardinDeck)
    #     db.session.commit()
    #     return updated_cardinDeck


