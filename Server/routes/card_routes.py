from flask import Blueprint, make_response , jsonify , request
from sqlalchemy.exc import SQLAlchemyError

#local imports
from models import Card
from utils.server_responseutils import paginate , server_error_response , item_not_found_response

cards_bp = Blueprint('cards', __name__)


@cards_bp.route('/getAllCards')
def get_all_cards():
    
    filter_mapping = {
        'name' : lambda value: Card.name.ilike(f'%{value}%'),
        'card_type' : lambda value: Card.card_type.ilike(f'%{value}%'), 
        'card_attribute' : lambda value: Card.card_attribute.ilike(f'%{value}%'),
        'card_race' : lambda value: Card.card_race.ilike(f'%{value}%')
        #'id' : lambda value: Card.id==value
    }

    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page',default=20,type=int)

    filters = []
    try:
        for key, value in request.args.items():
            if key in filter_mapping:
                filter_element = filter_mapping[key](value)
                filters.append(filter_element)

        filtered_cards = Card.query.filter(*filters)
        paginated_results = paginate(filtered_cards,page,per_page)
        
        card_list = [card.to_dict(rules=('-card_in_deck','-card_in_inventory','-card_on_banlist','-releaseSet','-card_in_set')) for card in paginated_results.items]

        response_data = {
            'cards' : card_list,
            'page' : page,
            'per_page' : per_page,
            'total_pages' : paginated_results.pages,
            'total_items' : paginated_results.total
        }
        response = make_response(jsonify(response_data), 200)        
    except SQLAlchemyError as se:
        error_message = f'Error w/ SQLAlchemy {se}'
        return server_error_response()
    except Exception as e:
        error_message = f'Error {e}'
        print(error_message)
        return make_response(jsonify({'error': error_message}), 500)
    return response

@cards_bp.route('/getSingleCard/<int:card_id>')
def get_single_card_id(card_id):
    card_info = Card.query.filter(Card.id==card_id).first()
    if card_info:
        response = make_response(jsonify(card_info.to_dict(rules=('-card_in_deck','-card_in_set.card_in_inventory','-card_on_banlist'))),200)
    else:
        response = item_not_found_response()
    return response    
