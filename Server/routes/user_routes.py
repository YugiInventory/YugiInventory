from flask import Blueprint, make_response , jsonify, request
from sqlalchemy.exc import SQLAlchemyError , IntegrityError
from psycopg2.errors import UniqueViolation
from repo.user_repo import UserRepository


#Local

from models import User, RefreshToken
from config import db
from utils.server_responseutils import server_error_response , item_not_found_response
from utils.tokenutils import token_required , authorize , is_authorized_to_modify, issue_jwt_token
from utils.constants import ALLOWED_ATTRIBUTES

user_bp = Blueprint('user', __name__)


@user_bp.route('/createUser', methods=['POST'])
def create_user():
    try:
        user_repo = UserRepository()
        data = request.get_json()
        new_user = user_repo.create_and_commit(username=data['username'],password=data['password'],email=data['email'])
        jwt_token = issue_jwt_token(new_user.username, new_user.id)
        refresh_token = RefreshToken.issue_refresh_token(new_user.id)
        new_user_dict = new_user.to_dict()
        new_user_dict['accessToken'] = jwt_token
        new_user_dict['refresh_token'] = refresh_token.token
        response = make_response(jsonify(new_user_dict),201)
    except SQLAlchemyError as se:
        print(se)
        response = server_error_response()
    except ValueError as ve:
        print(ve)
        response = make_response({'Error':'Failed to Create'},400)
    return response    

    # data = request.get_json()
    # try:
    #     new_user = User(
    #         username = data['username'],
    #         password_hash = data['password'],
    #         email = data['email']
    #     )
    #     db. session.add(new_user)
    #     db.session.commit()
    #     response = make_response({},201)
    # except SQLAlchemyError as se:
    #     print(se)
    #     response = server_error_response()
    # except ValueError as ve:
    #     print(ve)
    #     response = make_response({'Error':'Failed to Create'},400)
    
    # return response

@user_bp.route('/editUser', methods = ["PATCH"])
@token_required
def edit_user_parameters(user_id, **kwargs):
    data = request.get_json()
    user_to_edit = User.query.filter(User.id==user_id).first()
    for key , value in data.items():

        if key=='password':
            setattr(user_to_edit,'password_hash',value)

        if hasattr(user_to_edit, key) and key in ALLOWED_ATTRIBUTES["User"]:
            setattr(user_to_edit, key, value)
        try:
            db.session.add(user_to_edit)
            db.session.commit()
            response = make_response({},201)
        except SQLAlchemyError as se:
            print(se)
            db.session.rollback()
            response = server_error_response()   
        except ValueError as ve:
            print(ve)
            db.session.rollback()
            response = server_error_response()
    return response

@user_bp.route('/deleteUser' , methods = ["DELETE"])
@token_required
def delete_user(user_id):
    single_user = User.query.filter(User.id == user_id).first()
    if single_user():
        try:
            #Set up Cascade Delete
            db.session.delete(single_user)
            db.session.commit()
            response = make_response({},204)
        except SQLAlchemyError as se:
            print(se)
            db.session.rollback()
            response = server_error_response()
    else:
        response = item_not_found_response()
    return response

@user_bp.route('/getSingleUserInfo/<int:user_id>', methods = ["GET"])
def get_single_user_info(user_id):
    single_user = User.query.filter(User.id==user_id).first()
    if single_user:
        response = make_response(jsonify(single_user.to_dict(only=('created_at','profile','username'))), 200) #Rules to remove unnecessary information
    else:
        response = item_not_found_response()
    
    return response