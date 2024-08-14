from abc import ABC , abstractmethod

class ReadWriteRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id():
        pass

    @abstractmethod
    def add():
        pass

    @abstractmethod
    def update():
        pass

    @abstractmethod
    def delete():
        pass
    
    @abstractmethod
    def filter(self, **filters):
        pass

    @abstractmethod
    def paginate(self,query,page,per_page):
        pass


class ReadOnlyRepositoryInterface(ABC):

    @abstractmethod
    def get_by_id(self, id):
        pass

    @abstractmethod
    def filter(self, **filters):
        pass

    @abstractmethod
    def paginate(self, query, page, per_page):
        pass