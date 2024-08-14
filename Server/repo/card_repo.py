from .repository_interface import ReadOnlyRepositoryInterface
from models import Card
from flask_sqlalchemy import SQLAlchemy


class CardRepository(ReadOnlyRepositoryInterface):
    
    card_filter_mapping = {
        'name' : lambda value: Card.name.ilike(f'%{value}%'),
        'card_type' : lambda value: Card.card_type.ilike(f'%{value}%'), 
        'card_attribute' : lambda value: Card.card_attribute.ilike(f'%{value}%'),
        'card_race' : lambda value: Card.card_race.ilike(f'%{value}%')
    }


    def __init__(self):
        super().__init__(Card)

    
