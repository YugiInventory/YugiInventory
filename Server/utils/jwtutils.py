import jwt
import datetime

from flask import request , jsonify
from config import app
from functools import wraps


def issue_jwt_token(username,user_id):
    token = jwt.encode({'username':username,'user_id':user_id,'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)},app.config['SECRET_KEY'])            
    
    return token


def invalidate_jwt_token():
    pass

def handle_expired_jwt():
    pass

def validate_jwt():
    pass


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
            print('Auth in here')
        if not token:
            return jsonify({'message': 'No Token'}), 401
        
        try:
            print(token)
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            print(data)
            user_id = data['user_id']
        except Exception as e:
            print(e)
            return jsonify({"message":"invalid token"}), 401
        
        return f(user_id, *args, **kwargs)
    return decorated