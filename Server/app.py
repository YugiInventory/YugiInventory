#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request, session
import os
import uuid
import jwt
import datetime
from sqlalchemy.exc import SQLAlchemyError

# Local imports
from models import *
from config import app, db
from models import User, Card, Deck, CardinSet, Banlist, BanlistCard , RefreshToken
from utils.tokenutils import issue_jwt_token , token_required

from routes.auth_routes import auth_bp
from routes.card_routes import cards_bp
from routes.set_routes import set_bp
from routes.user_routes import user_bp
from routes.inventory_routes import inventory_bp
from routes.deck_routes import deck_bp
from routes.cardindeck_routes import cardinDeck_bp
from routes.reconcile_routes import reconcile_bp

app.register_blueprint(auth_bp, url_prefix = '/auth')
app.register_blueprint(cards_bp, url_prefix = '/cards')
app.register_blueprint(set_bp, url_prefix = '/sets')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(inventory_bp, url_prefix='/inventory')
app.register_blueprint(deck_bp , url_prefix='/deck')
app.register_blueprint(cardinDeck_bp, url_prefix="/cardinDeck")
app.register_blueprint(reconcile_bp)

###Helper Functions####
# def server_error_response():
#     return jsonify({'Error': 'Server Error'}),500

# def item_not_found_response():
#     return jsonify({'Error': 'Item not found'}), 404

# def validation_error_response():
#     return jsonify({'Error': 'Validation Error'}), 403

# def bad_request_response():
#     return jsonify({'Error':'Bad Request'}),400
# #item_not_found_response = make_response({'Error':'Item not found'},404)

# def paginate(query,page, per_page):
#     return query.paginate(page=page,per_page=per_page) #these all have to be deinfed with keyword only?


# def invalidate_refresh_token(user_id):
#     #this would be deleted from the server
#     refreshToken = RefreshToken.query.filter(RefreshToken.user_id == user_id).first()
#     if refreshToken:
#         db.session.delete(refreshToken)
#         db.session.commit()
#         return True
#     return False


# def handle_expired_jwt(token, key, refreshToken=None):
#     expired_payload = jwt.decode(token,key=key, algorithms = ["HS256"], verify=False)
#     if refreshToken:
#         #check if valid refresh
#         known_token = RefreshToken.query.filter(RefreshToken.user_id==expired_payload.user_id).first()
#         if known_token and known_token.token == refreshToken:
#             new_JWT_Token = issue_jwt_token(expired_payload.username, expired_payload.user_id)
#             return new_JWT_Token, expired_payload
#         else:
#             #Expired JWT and Invalid Refresh require relogin and destroy saved refresh token.
#             invalidate_refresh_token(expired_payload.user_id)
#     else:
#         #Error require relog no Refresh Token
#         pass
#     return None, None , None

# def validate_jwt(token, key = app.config['SECRET_KEY'], refreshToken = None):
#     try:
#         decoded_token = jwt.decode(token,key,algorithms=["HS256"])
#         return decoded_token
#     except jwt.ExpiredSignatureError:
#         new_jwt, decoded_payload = handle_expired_jwt(token=token,key=key,refreshToken=refreshToken)
#         if new_jwt:
#             return decoded_payload
#     except jwt.InvalidTokenError:
#         pass


@app.route('/')
def home():
    return 'homse'

####################Card Queries####################3333
# @app.route('/cards') #Load all card info. 
# def cards():

#     filter_mapping = {
#         'name' : lambda value: Card.name.ilike(f'%{value}%'),
#         'card_type' : lambda value: Card.card_type.ilike(f'%{value}%'), 
#         'card_attribute' : lambda value: Card.card_attribute.ilike(f'%{value}%'),
#         'card_race' : lambda value: Card.card_race.ilike(f'%{value}%')
#         #'id' : lambda value: Card.id==value
#     }

#     page = request.args.get('page', default=1, type=int)
#     per_page = request.args.get('per_page',default=20,type=int)

#     filters = []
#     try:
#         for key, value in request.args.items():
#             if key in filter_mapping:
#                 filter_element = filter_mapping[key](value)
#                 filters.append(filter_element)

#         filtered_cards = Card.query.filter(*filters)
#         paginated_results = paginate(filtered_cards,page,per_page)
        
#         card_list = [card.to_dict(rules=('-card_in_deck','-card_in_inventory','-card_on_banlist','-releaseSet','-card_in_set')) for card in paginated_results.items]

#         response_data = {
#             'cards' : card_list,
#             'page' : page,
#             'per_page' : per_page,
#             'total_pages' : paginated_results.pages,
#             'total_items' : paginated_results.total
#         }
#         response = make_response(jsonify(response_data), 200)        
#     except SQLAlchemyError as se:
#         error_message = f'Error w/ SQLAlchemy {se}'
#         return server_error_response()
#     except Exception as e:
#         error_message = f'Error {e}'
#         print(error_message)
#         return make_response(jsonify({'error': error_message}), 500)
#     return response


# @app.route('/card/<int:card_id>')
# def card(card_id): #Single Card
#     card_info = Card.query.filter(Card.id==card_id).first()
#     if card_info:
#         response = make_response(jsonify(card_info.to_dict(rules=('-card_in_deck','-card_in_set.card_in_inventory','-card_on_banlist'))),200)
#     else:
#         response = item_not_found_response()
#     return response


##########SET QUERIES#####################3
#View all sets
#Get a single Set by id

# @app.route('/sets')
# def sets():

#     filter_mapping = {
#         'name' : lambda value: ReleaseSet.name.ilike(f'%{value}%'),
#         #'releaseDate' : lambda value: .card_type.ilike(f'%{value}%'), 
#         'set_code' : lambda value: Card.card_attribute.ilike(f'%{value}%')
#     }

#     set_info = ReleaseSet.query.all()
#     set_list = [pack.to_dict(only=('name','card_count','id','releaseDate','set_code')) for pack in set_info]
#     response = make_response(jsonify(set_list),200)
#     return response

# @app.route('/set/<int:set_id>')
# def set_single(set_id):
#     try:
#         set_info = ReleaseSet.query.filter(ReleaseSet.id==set_id).first()
#         response = make_response(jsonify(set_info.to_dict(rules=('-card_in_set.card.card_in_deck','-card_in_set.card.card_on_banlist','-card_in_set.card_in_inventory','-card_in_set.releaseSet','card_in_set.releaseSet.id'))),200)
#         #card image, id only thing we need from the card section. 
#     except SQLAlchemyError as se:
#         print(se)
#         response = server_error_response()
#     return response

##########User Related Queries##############################3


# @app.route('/user', methods = ['POST','PATCH','DELETE'])
# def user():
#     data = request.get_json()
#     if request.method == 'POST':
#         try:
#             new_user = User(
#                 username = data['username'],
#                 password_hash = data['password'],
#                 email = data['email']
#             )
#             db.session.add(new_user)
#             db.session.commit()
#             response = make_response({},200)
#         except SQLAlchemyError as se:
#             print(se)
#             response = server_error_response()
#         except ValueError as ve:
#             print(ve)
#             response = make_response({'Error':'Failed to Create'},400)
#     elif request.method == 'PATCH': #{"id":1, "username" : "shamallama"}
#         single_user = User.query.filter(User.id == data['id']).first()
#         if single_user:
#             for key, value in data.items():
#                 if hasattr(single_user, key):
#                     setattr(single_user, key, value) 
#             try:
#                 db.session.add(single_user)
#                 db.session.commit()
#                 response = make_response({},200) #should send back information to update page yes or no? 
#             except SQLAlchemyError as se:
#                 print(se)
#                 db.session.rollback()
#                 response = server_error_response()
#         else:
#             response = item_not_found_response()
#     elif request.method == 'DELETE':
#         single_user = User.query.filter(User.id == data['id']).first()
#         if single_user:
#             try:
#                 db.session.delete(single_user) #Set up cascade delete
#                 db.session.commit()
#                 response = make_response({},204)
#             except SQLAlchemyError as se:
#                 print(se)
#                 db.session.rollback()
#                 response = server_error_response()
#         else:
#             response = item_not_found_response()
#     return response

# @app.route('/users/<int:id>' , methods = ['GET'])
# def getUser(id):
#     single_user = User.query.filter(User.id==id).first()
#     if single_user:
#         response = make_response(jsonify(single_user.to_dict(only=('created_at','profile','username'))), 200) #Rules to remove unnecessary information
#     else:
#         response = item_not_found_response()
    
#     return response

######Inventory Queries######################

# @app.route('/inventory/<int:id>', methods = ['GET', 'DELETE'])
# def Userinventory(id):

#     filter_mapping = {
#         'name': lambda value: Card.name.contains(value) , #SQLalchemy binary expression type is the returnfrom lambda function
#         'card_code' : lambda value: CardinSet.card_code.contains(value),
#         'rarity' : lambda value: CardinSet.rarity.ilike(f'%{value}%'),
#         'card_type' : lambda value: Card.card_type.ilike(f'%{value}%'), 
#     }

#     skip_keys = ['page', 'per_page']
    
#     if request.method == 'GET':
#         try:                
#             inventory_filtered_query = Inventory.query.filter(Inventory.user_id == id) #Base Query we need to add filter parameters
            
#             for key, value in request.args.items():
#                 if key in filter_mapping:
#                     filter_element = filter_mapping[key](value)
#                     inventory_filtered_query = inventory_filtered_query.filter(filter_element)

#             page = request.args.get('page', default=1,type=int)
#             per_page = request.args.get('per_page', default=20,type=int)
#             paginated_inventory = paginate(inventory_filtered_query,page,per_page)

#             card_list = [card.to_dict(rules=('-cardinSet.card.card_in_deck','-user','-cardinSet.releaseSet','-cardinSet.releaseSet.id''-cardinSet.card.card_on_banlist','-cardinSet.card')) for card in paginated_inventory.items]

#             response_data = {
#                 'cards': card_list,
#                 'page': page,
#                 'per_page' : per_page,
#                 'total_pages' : paginated_inventory.pages,
#                 'total_items' : paginated_inventory.total
#              }
#             response = make_response(jsonify(response_data),200)
#         except SQLAlchemyError as se:
#             error_message = f'Error w/ SQLAlchemy {se}'
#             return server_error_response()
#         except Exception as e:
#             error_message = f'Error {e}'
#             return make_response(jsonify({'error': error_message}), 500)
#     else:

#         pass 

#     return response


#####CardinInventory#######
#Add a card in inventory
#Delete a card in Inventory
#Modify a card in Inventory 

# @app.route('/CardinInventory', methods = ['POST', 'PATCH', 'DELETE'])
# def modify_Card_in_Inventory():
#     data = request.get_json() #Set code and rarity are necessary to find correct CardinSet_id

#     if request.method == 'POST':
#         #{"quantity": 3, "user_id" : 1, "isFirstEd" : false, "rarity" : "Ghost Rare", "card_id":"TDGS-EN040"} Test on reqbin
#         card_to_make = CardinSet.query.filter(CardinSet.card_code==data['card_id'],CardinSet.rarity==data['rarity']).first()
#         if card_to_make:
            
#             isduplicate = Inventory.query.filter(Inventory.cardinSet_id==card_to_make.id,Inventory.user_id==data['user_id'],Inventory.isFirstEd==data['isFirstEd']).first()

#             if isduplicate:
#                 new_q = int(isduplicate.quantity) + int(data['quantity'])
#                 isduplicate.quantity = new_q
#                 try:
#                     db.session.add(isduplicate)
#                     db.session.commit()
#                     response = make_response({'Duplicate Entry':'combined quantity'}, 250)
#                 except SQLAlchemyError as se:
#                     print(se)
#                     response = server_error_response()
#             else:
#                 try:
#                     new_inventory_record = Inventory(
#                         quantity = data['quantity'],
#                         isFirstEd = data['isFirstEd'],
#                         user_id = data['user_id'],
#                         cardinSet_id = card_to_make.id
#                     )
#                     db.session.add(new_inventory_record)
#                     db.session.commit()
#                     response = make_response({'Sucess': 'Card Added'},201)
#                 except ValueError as ve:
#                     print(ve)
#                     response = bad_request_response()
#                 except SQLAlchemyError as se:
#                     print(se)
#                     db.session.rollback()
#                     response = server_error_response()
#         else:
#             response = item_not_found_response()
    
#     elif request.method == 'DELETE':
#         #depends on how the info is on the front, we can delete with id or delete from card_id_rarity_id owned. 
#         card = Inventory.query.filter(Inventory.id == data['id']).first()
#         try:
#             db.session.delete(card)
#             db.session.commit()
#             response = make_response({},204)
#         except SQLAlchemyError as se:
#             print(se)
#             db.session.rollback()
#             response = server_error_response()
    
#     elif request.method == 'PATCH':
#         owned_card = Inventory.query.filter(Inventory.id == data['id']).first() #I could edit somebody else card if the wrong id is sent
#         for key, value in data.items():
#             if hasattr(owned_card, key):
#                 setattr(owned_card, key, value) 
#         try:
#             db.session.add(owned_card)
#             db.session.commit()
#             response = make_response({},200) #should send back information to update page yes or no?, no since we already have that value stored in the front end. 
#         except SQLAlchemyError as se:
#             print(se)
#             db.session.rollback()
#             response = server_error_response()
#     return response

##########Deck Queries####################3
#Create a Deck
#Get a Deck

# @app.route('/deck' , methods = ['POST' , 'PATCH' , 'DELETE'])
# def deck():

#     data = request.get_json()

#     if request.method == 'POST':
#         try:
#             new_deck = Deck(
#                 isPublic = True,
#                 user_id = data['user_id'],
#                 name = data['name']
#             )
#             db.session.add(new_deck)
#             db.session.commit()
#             response = make_response({'Sucess' : 'Deck created'},201)
#         except SQLAlchemyError as se:
#             db.session.rollback()
#             print(se)
#             response = server_error_response
#     elif request.method == 'DELETE':   ##might have to be its own thing for some servers, DELETe shouldnt havea  request body and be able to find everything with the URI 
#         single_deck = Deck.query.filter(Deck.id==data['deck_id']).first()
#         if single_deck:
#             cards_in_deck = CardinDeck.query.filter(CardinDeck.deck_id==data['deck_id']).all()
#             try:
#                 for single_card in cards_in_deck:
#                     db.session.delete(single_card)
#                 db.session.delete(single_deck)
#                 db.session.commit()
#                 response = make_response({},204)
#             except SQLAlchemyError as se:
#                 db.session.rollback()
#                 print(se)
#                 response = server_error_response()
#         else:
#             response = item_not_found_response() #404 Deck not found
#     elif request.method == 'PATCH':
#         single_deck = Deck.query.filter(Deck.id==data['deck_id']).first()
#         if single_deck:
#             for key,value in data.items():
#                 if hasattr(single_deck,key):
#                     setattr(single_deck,key,value)
#             try:
#                 db.session.add(single_deck)
#                 db.session.commit()
#                 response = make_response({'Sucess':'Updated'},202)
#             except SQLAlchemyError as se:
#                 db.session.rollback()
#                 print(se)
#                 response = server_error_response()
#         else:
#             response = item_not_found_response()
#     return response

# @app.route('/decks', methods = ['GET'])
# def decks():

#     filter_mapping = {
#         'user_id' : lambda value: Deck.user_id==value,
#         'name' : lambda value: Deck.name.ilike(f'%{value}%'),
#         'id' : lambda value: Deck.id==value
#     }

#     try:
#         filter_elements = []
#         for key,value in request.args.items():
#             filter_element = filter_mapping[key](value)   
#             filter_elements.append(filter_element)
#         decks_list = Deck.query.filter(*filter_elements).all()
#         deck_list = [deck.to_dict(rules=('-card_in_deck','-user'))for deck in decks_list]
#         response = make_response(jsonify(deck_list), 200)
#     except SQLAlchemyError as se:
#         print(se)
#         response = server_error_response()
#     return response

# @app.route('/singleDeck/<int:deck_id>', methods = ['GET']) #When we want to display a deck info so we pass in the deck cards and etc
# def singleDeck(deck_id):
#     single_deck = Deck.query.filter(Deck.id == deck_id).first()

#     if single_deck:
#         try:
#             response = make_response(jsonify(single_deck.to_dict()),200)
#         except SQLAlchemyError as se:
#             print(se)
#             response = server_error_response()
#     else:
#         response = item_not_found_response()
#     return response



#####CardinDeck########
#Add a card in Deck
#Delete a card in Deck
#Modify a card in Deck

# @app.route('/CardinDeck', methods = ['POST', 'PATCH', 'DELETE'])
# def modify_Card_in_Deck():
#     data = request.get_json()

#     if request.method == 'POST':
#         card_to_add = Card.query.filter(Card.id==data['card_id']).first()
#         if card_to_add:
#             try:
#                 new_card_in_deck = CardinDeck(
#                     quantity = data['quantity'],
#                     location = data['location'],
#                     deck_id = data['deck_id'],
#                     card_id = card_to_add.id
#                 )
#                 db.session.add(new_card_in_deck)
#                 db.session.commit()
#                 response = make_response({'Sucess': 'Card Added'}, 201)
#             except ValueError as ve:
#                 print(ve)
#                 response = validation_error_response()
#             except SQLAlchemyError as se:
#                 print(se)
#                 db.session.rollback()
#                 response = server_error_response()
#         else:
#             response = item_not_found_response()
#     elif request.method == 'PATCH':
#         card_in_deck = CardinDeck.query.filter(CardinDeck.id == data['card_in_deck_id']).first()
#         for key,value in data.items():
#             if hasattr(card_in_deck,key):
#                 setattr(card_in_deck,key,value)
#             try:
#                 db.session.add(card_in_deck)
#                 db.session.commit()
#                 response = make_response({},200)
#             except SQLAlchemyError as se:
#                 print(se)
#                 db.session.rollback()
#                 response = server_error_response()
#     elif request.method == 'DELETE':
#         card_in_deck = CardinDeck.query.filter(CardinDeck.id == data['card_in_deck_id']).first()
#         try:
#             db.session.delete(card_in_deck)
#             db.session.commit()
#             response = make_response({},204)
#         except SQLAlchemyError as se:
#             print(se)
#             db.session.rollback()
#             response = server_error_response()
#     return response


######Reconciliation Routes################

# @app.route('/InventRecon/<int:userid>', methods = ['POST'])
# def ReconDecks(userid):
#     #Get a list of deck ids that we want to reconcile against
#     deck_list = request.get_json() #list of decks 


#     base = db.session.query(Inventory)
#     invent = base.filter(Inventory.user_id==userid).outerjoin(CardinSet,Inventory.cardinSet_id==CardinSet.id).outerjoin(Card,CardinSet.card_id==Card.id)
#     id_count = {}
#     cards_by_deck = {}  

#     for val in deck_list: #[1,2]
#         cards_in_deck = CardinDeck.query.filter(CardinDeck.deck_id==val).all() #[1,2,3,4,5]
        
        
#         deck_name = db.session.query(Deck.name).filter(Deck.id==val).scalar()  #Blackwing 
        
#         for card in cards_in_deck: 

#             id_count[card.card_id] = id_count.get(card.card_id,0) + card.quantity #if it doesnt exist its 0+ quantity, 
#             cards_by_deck.setdefault(card.card_id, []).append((card.quantity, deck_name, val)) #if it doesnt exist we set it to the empty list then add the tuple


#     #Now we have all the cards, lets compare it against the users inventory
            
#     recon_array = []
#     for card_id,quantity in id_count.items():

#         cards_owned = invent.filter(Card.id==card_id).all() #all copies of the card
#         c_name = db.session.query(Card.name).filter(Card.id==card_id).first()[0]
        
#         owned_quantity = sum(record.quantity for record in cards_owned) if cards_owned else 0
#         needed = max(0,quantity-owned_quantity)

#         data_obj = {
#             'name': c_name,
#             'id' : card_id,
#             'owned': owned_quantity,
#             'required' : quantity,
#             'need' : needed,
#             'usage' : cards_by_deck[card_id]
#         }

#         recon_array.append(data_obj)

#     response = make_response(jsonify(recon_array), 200)
#     return response

# @app.route('/Login', methods = ['POST'])
# def Login():    

#     user_info = request.get_json()     
    
#     user = User.query.filter(User.username == user_info['username']).first()

#     if 'refreshToken' in user_info:
#         #Check if refreshToken is Valid
#         #If Valid return an access Token
#         issue_jwt_token()
#         pass

#     if user:
#         pass_match = user.authenticate(user_info['password'])
#         if pass_match:
#             #create JWT and refresh token
#             #token = issue_jwt_token(user.username,user.id)            
#             # refresh_token = issue_refresh_token(user.id)
            
#             token = issue_jwt_token(user.username, user.id)
#             refresh_token = RefreshToken.issue_refresh_token(user.id)

#             #If we have a refresh token we need to just update that param

#             has_refresh = RefreshToken.query.filter(RefreshToken.user_id == user.id).first()

#             if has_refresh:
#                 has_refresh.token, has_refresh.expiration_time = refresh_token.token, refresh_token.expiration_time
#                 db.session.add(has_refresh)
#             else:
#                 db.session.add(refresh_token)
            
#             db.session.commit()
            
#             user_dict = user.to_dict()
#             user_dict['accessToken'] = token
#             user_dict['refreshToken'] = refresh_token.token
#             response = make_response( 
#                 jsonify(user_dict), 201
#             )
#         else:
#            response = make_response({},401)
#     else:
#         response = make_response({},404)
    
#     return response

# @app.route('/Logout', methods = ["POST"])
# def logout():
#     #Send back the user id, delete that entry from the refreshToken table. 
#     data = request.get_json()
#     #expect the user_id 

#     isLogOut = invalidate_refresh_token(data['user_id'])
#     if isLogOut:
#         response = make_response({},200)
#         return response
#     return make_response({},401)

# @app.route('/Refresh', methods = ["POST"])
# def refresh_token():
#     #Send a refresh token to the server, and get out a new access token
#     pass


# @app.route('/TestAuth', methods=['GET'])
# @token_required
# def user_invent(user_id):
#     card_info = Inventory.query.filter(Inventory.user_id==user_id).first()
#     print('???')

#     response = make_response(jsonify(card_info)),201
#     return response

if __name__ == '__main__':

    app.run(port=5555, debug=True)


