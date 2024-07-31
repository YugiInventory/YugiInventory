from flask import Blueprint, make_response , jsonify



user_bp = Blueprint('/user', __name__)


@user_bp.route('/create', methods=['POST'])
def create_user():
    pass