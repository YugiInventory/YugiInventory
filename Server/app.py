#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from models import *
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request, session
import os
from sqlalchemy.exc import SQLAlchemyError

# Local imports

from config import app, db
from models import User, Card, Deck, CardinSet, Banlist, BanlistCard

haha = '123'

@app.route('/')
def home():
    return 'test'

@app.route('/t2')
def home2():
    return 'jajaja'

@app.route('/users')
def users():
    userinfo = db.session.query(User).all()
    user_list = []
    for user in userinfo:
        user_list.append(user.to_dict())
    
    response = make_response(jsonify(user_list),200)
    return response


####################Card Queries####################3333
def paginate(query,page, per_page):
    return query.paginate(page=page,per_page=per_page) #these all have to be deinfed with keyword only?

@app.route('/cards') #Load all card info. 
def cards():

    filter_mapping = {
        'name' : lambda value: Card.name.ilike(f'%{value}%'),
        'card_type' : lambda value: Card.card_type.ilike(f'%{value}%'), 
        'card_attribute' : lambda value: Card.card_attribute.ilike(f'%{value}%'),
        'card_race' : lambda value: Card.card_race.ilike(f'%{value}%'), 
        'id' : lambda value: Card.id==value
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
        return make_response(jsonify({'error': error_message}), 500)
    except Exception as e:
        error_message = f'Error {e}'
        return make_response(jsonify({'error': error_message}), 500)
    return response


@app.route('/card/<int:card_id>')
def card(card_id): #Single Card
    card_info = Card.query.filter(Card.id==card_id).first()
    if card_info:
        response = make_response(jsonify(card_info.to_dict(rules=('-card_in_deck','-card_in_set.card_in_inventory'))),200)
    else:
        response = make_response({},404)
    return response
##########SET QUERIES#####################3

##########Deck Queries####################3

##########User Related Queries##############################3


######3Inventory Queries######################


@app.route('/inventory<int:id>', methods = ['GET', 'DELETE'])
def Userinventory(id):

    filter_mapping = {
        'name': lambda value: Card.name.contains(value) , #SQLalchemy binary expression type is the returnfrom lambda function
        'card_code' : lambda value: CardinSet.card_code.contains(value),
        'rarity' : lambda value: CardinSet.rarity.ilike(f'%{value}%'),
        'card_type' : lambda value: Card.card_type.ilike(f'%{value}%'), 
    }

    skip_keys = ['page', 'per_page']
    
    if request.method == 'GET':
        try:                
            inventory_filtered_query = Inventory.query.filter(Inventory.user_id == id) #Base Query we need to add filter parameters
            
            for key, value in request.args.items():
                if key in filter_mapping:
                    filter_element = filter_mapping[key](value)
                    inventory_filtered_query = inventory_filtered_query.filter(filter_element)

            page = request.args.get('page', default=1,type=int)
            per_page = request.args.get('per_page', default=20,type=int)
            paginated_inventory = paginate(inventory_filtered_query,page,per_page)

            card_list = [card.to_dict(rules=('-cardinSet.card.card_in_deck',)) for card in paginated_inventory.items]

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
            return make_response(jsonify({'error': error_message}), 500)
        except Exception as e:
            error_message = f'Error {e}'
            return make_response(jsonify({'error': error_message}), 500)
    else:
        pass #DELETE inventory 

    return response

######Reconciliation Routes################

@app.route('/InventRecon/<int:userid>', methods = ['POST'])
def ReconDecks(userid):
    #Get a list of deck ids that we want to reconcile against
    deck_list = request.get_json() #list of decks 


    base = db.session.query(Inventory)
    invent = base.filter(Inventory.user_id==userid).outerjoin(CardinSet,Inventory.cardinSet_id==CardinSet.id).outerjoin(Card,CardinSet.card_id==Card.id)
    id_count = {}
    cards_by_deck = {}  

    for val in deck_list: #[1,2]
        cards_in_deck = CardinDeck.query.filter(CardinDeck.deck_id==val).all() #[1,2,3,4,5]
        deck_name = db.session.query(Deck.name).filter(Deck.id==val).scalar()  #Blackwing 
        
        for card in cards_in_deck: 

            id_count[card.card_id] = id_count.get(card.card_id,0) + card.quantity #if it doesnt exist its 0+ quantity, 
            cards_by_deck.setdefault(card.card_id, []).append((card.quantity, deck_name, val)) #if it doesnt exist we set it to the empty list then add the tuple


    #Now we have all the cards, lets compare it against the users inventory
            
    recon_array = []
    for card_id,quantity in id_count.items():

        cards_owned = invent.filter(Card.id==card_id).all() #all copies of the card
        c_name = db.session.query(Card.name).filter(Card.id==card_id).first()[0]
        
        owned_quantity = sum(record.quantity for record in cards_owned) if cards_owned else 0
        needed = max(0,quantity-owned_quantity)

        data_obj = {
            'name': c_name,
            'id' : card_id,
            'owned': owned_quantity,
            'required' : quantity,
            'need' : needed,
            'usage' : cards_by_deck[card_id]
        }

        recon_array.append(data_obj)

    response = make_response(jsonify(recon_array), 200)
    return response


if __name__ == '__main__':

    app.run(port=5555, debug=True)
