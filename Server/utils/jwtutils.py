import jwt
import datetime

from config import app

def issue_jwt_token(username,user_id):
    token = jwt.encode({'username':username,'user_id':user_id,'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=15)},app.config['SECRET_KEY'])            
    
    return token


def invalidate_jwt_token():
    pass

def handle_expired_jwt():
    pass

def validate_jwt():
    pass