from abc import ABC , abstractmethod

class ReadWriteRepositoryInterface(ABC):

    def __init__(self, model):
        self.model = model


    @abstractmethod
    def add():
        pass

    @abstractmethod
    def update():
        pass

    @abstractmethod
    def delete():
        pass
        
    def get_by_id(self,id):
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

    @abstractmethod
    def get_by_id(self, id):
        pass

    def get_by_id(self,id):
        query = self.model.query.filter(self.model.id==id)
        return query

    def filter(self, *filters):
        query = self.model.query
        query = query.filter(*filters)
        return query
    
    def paginate(self,query,page=1,per_page=20):
        return query.paginate(page=page, per_page=per_page)