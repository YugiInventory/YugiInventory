from repository_interface import ReadOnlyRepositoryInterface

from models import Card
from flask_sqlalchemy import SQLAlchemy


class CardRepository(ReadOnlyRepositoryInterface):
    
    def get_by_id(self, id):
        return super().get_by_id(id)
    
    def filter(self, **filters):
        query = Card.query
        for key , value in filters.items():
            if hasattr(Card,key):
                query = query.filter(getattr(Card,key).ilike(f'%{value}%'))
        return query
    
    def paginate(self, query, page, per_page):
        return super().paginate(query, page, per_page)