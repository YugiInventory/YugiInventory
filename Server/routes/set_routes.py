from flask import Blueprint, make_response , jsonify , request
from sqlalchemy.exc import SQLAlchemyError


from models import ReleaseSet, Card
from utils.server_responseutils import server_error_response
from utils.flaskutils import get_filter_params
from repo.Releasesets_repo import ReleaseSetsRepository


set_bp = Blueprint('sets',__name__)

@set_bp.route('/getAllSets')
def get_all_sets_info():
    #load minimal info
    try:
        filters = get_filter_params(ReleaseSetsRepository,request.args)
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page',default=20,type=int)        

        repo = ReleaseSetsRepository()
        query = repo.filter(*filters)
        paginated_results = repo.paginate(query,page=page,per_page=per_page)

        set_list = [pack.to_dict(only=('name','card_count','id','releaseDate','set_code')) for pack in paginated_results]
        
        response_data = {
            'sets' : set_list,
            'page' : page,
            'per_page' : per_page,
            'total_pages' : paginated_results.pages,
            'total_items' : paginated_results.total
        }

        response = make_response(jsonify(response_data),200)
    except SQLAlchemyError as se:
        print(se)
        response = server_error_response()
    return response


@set_bp.route('/getSingleSet/<int:set_id>')
def get_single_set_info(set_id):
    try:
        set_info = ReleaseSet.query.filter(ReleaseSet.id==set_id).first()
        response = make_response(jsonify(set_info.to_dict()),200)   #rules=('-card_in_set.card.card_in_deck','-card_in_set.card.card_on_banlist','-card_in_set.card_in_inventory','-card_in_set.releaseSet','card_in_set.releaseSet.id')
        #card image, id only thing we need from the card section. 
    except SQLAlchemyError as se:
        print(se)
        response = server_error_response()
    return response