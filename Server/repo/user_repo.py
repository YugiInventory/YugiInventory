from .repository_interface import ReadWriteRepositoryInterface
from models import User
from config import db


class UserRepository(ReadWriteRepositoryInterface):

    search_filters = {
        'name_partial' : lambda value: User.username.ilike(f'%{value}%')
    }

    def create(self,username,password,email):
        new_user = User(
            username = username,
            password_hash = password,
            email = email
        )
        db.session.add(new_user)
        return new_user
    
    def create_and_commit(self,username,password,email):
        new_user = self.create(username,password,email)
        db.session.commit()
        return new_user
    
    def __init__(self):
        super().__init__(User)