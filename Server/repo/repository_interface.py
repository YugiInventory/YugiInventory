from abc import ABC , abstractmethod
from collections import namedtuple

OperationResult = namedtuple('OperationResult',['status','return_data'])

class ReadWriteRepositoryInterface(ABC):
    def __init__(self, model):
        self.model = model


    @abstractmethod
    def create():
        pass

    @abstractmethod
    def update():
        pass

    @abstractmethod
    def delete():
        pass
        
    def get_item_by_id(self,id):
        q = self.get_query_by_id(id)
        return q.first_or_404()
    
    def get_query_by_id(self,id):
        query = self.model.query.filter(self.model.id==id)
        return query

    def filter(self, *filters):
        query = self.model.query
        query = query.filter(*filters)
        return query
    
    def paginate(self,query,page=1,per_page=20):
        return query.paginate(page=page, per_page=per_page)


class ReadOnlyRepositoryInterface(ABC):

    def __init__(self, model):
        self.model = model
    
    def get_item_by_id(self,id):
        q = self.get_query_by_id(id)
        return q.first_or_404()
    
    def get_query_by_id(self,id):
        query = self.model.query.filter(self.model.id==id)
        return query

    def filter(self, *filters):
        query = self.model.query
        query = query.filter(*filters)
        return query
    
    def paginate(self,query,page=1,per_page=20):
        return query.paginate(page=page, per_page=per_page)
    
