from .repository_interface import ReadWriteRepositoryInterface , OperationResult
from models import Deck
from flask_sqlalchemy import SQLAlchemy
from config import db
from sqlalchemy.exc import SQLAlchemyError

class DeckRepository(ReadWriteRepositoryInterface):
    
    filter_mapping = {
        'user_id' : lambda value: Deck.user_id==value,
        'name' : lambda value: Deck.name.ilike(f'%{value}%'),
    }

    def __init__(self):
        super().__init__(Deck)

    def create(self, user_id, name , is_public=True):
        try:
            print('tryna make a deck')
            new_deck = Deck(
                name = name,
                user_id = user_id,
                isPublic = is_public
            )
            print('tryna add deck')
            db.session.add(new_deck)
            print('jaja')
            return OperationResult(True, new_deck)
        except Exception as e:
            print('errr we here?')
            db.session.rollback()
            return OperationResult(False, e)
    
    def create_and_commit(self, user_id, name , is_public=True):
        try:
            new_deck = Deck(
                name = name,
                user_id = user_id,
                isPublic = is_public
            )
            db.session.add(new_deck)
            db.session.commit()
            return OperationResult(True, new_deck)
        except Exception as e:
            db.session.rollback()
            return OperationResult(False,e)

    def delete():
        pass

    def update():
        pass
        