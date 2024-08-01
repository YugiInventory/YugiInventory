from flask import Blueprint, make_response , jsonify , request
from sqlalchemy.exc import SQLAlchemyError

#Local imports
from utils.tokenutils import token_required
from utils.server_responseutils import paginate , server_error_response
from models import Card, CardinSet, Inventory


inventory_bp = Blueprint('/inventory', __name__)


@inventory_bp.route('/getUserInventory', methods = ["GET"])
@token_required
def getinventory(user_id):
    filter_mapping = {
        'name': lambda value: Card.name.contains(value) , #SQLalchemy binary expression type is the returnfrom lambda function
        'card_code' : lambda value: CardinSet.card_code.contains(value),
        'rarity' : lambda value: CardinSet.rarity.ilike(f'%{value}%'),
        'card_type' : lambda value: Card.card_type.ilike(f'%{value}%'), 
    }

    skip_keys = ['page', 'per_page']
    
    if request.method == 'GET':
        try:                
            inventory_filtered_query = Inventory.query.filter(Inventory.user_id == user_id) #Base Query we need to add filter parameters
            
            for key, value in request.args.items():
                if key in filter_mapping:
                    filter_element = filter_mapping[key](value)
                    inventory_filtered_query = inventory_filtered_query.filter(filter_element)

            page = request.args.get('page', default=1,type=int)
            per_page = request.args.get('per_page', default=20,type=int)
            paginated_inventory = paginate(inventory_filtered_query,page,per_page)

            card_list = [card.to_dict(rules=('-cardinSet.card.card_in_deck','-user','-cardinSet.releaseSet','-cardinSet.releaseSet.id''-cardinSet.card.card_on_banlist','-cardinSet.card')) for card in paginated_inventory.items]

            response_data = {
                'cards': card_list,
                'page': page,
                'per_page' : per_page,
                'total_pages' : paginated_inventory.pages,
                'total_items' : paginated_inventory.total
             }
            response = make_response(jsonify(response_data),200)
        except SQLAlchemyError as se:
            error_message = f'Error w/ SQLAlchemy {se}'
            return server_error_response()
        except Exception as e:
            error_message = f'Error {e}'
            return make_response(jsonify({'error': error_message}), 500)
    else:

        pass 

    return response

@inventory_bp.route('/deleteUsersInventory', methods = ["Delete"])
@token_required
def delete_Inventory(user_id):
    pass

@inventory_bp.route('/addCardToUserInventory', methods = ["POST"])
@token_required
def add_card_to_inventory(user_id):
    pass

@inventory_bp.route('/editCardInUserInventory', methods = ["PATCH"])
@token_required
def edit_card_to_inventory(user_id):
    pass

@inventory_bp.route('/deleteCardInUserInventory', methods = ["DELETE"])
@token_required
def edit_card_to_inventory(user_id):
    pass

