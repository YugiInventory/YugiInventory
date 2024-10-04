import requests
import pickle
import logging
from db_utils.helper import createDBReleaseSet , createDBcardSkeleton , createDBAltArt, toggleDBcardSkeletonbools
from config import db , app
from models import CardinSet 


card_endpoint = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
set_endpoint = 'https://db.ygoprodeck.com/api/v7/cardsets.php'

logging.basicConfig(
    filename = 'card_in_Set_Error.log',
    level = logging.WARNING,
    format='%(levelname)s - %(message)s'  # Log format
  
)


def init_seed_db():
    #Seed the DB using the ygproAPI
    #Creating the Release Sets
    #set_name_id_map = create_release_sets()
    response = requests.get(set_endpoint)
    sets_info = response.json()
    set_to_id_map = {}
    for card_set in sets_info:
        pack_db_id,pack_name,pack_release_date = createDBReleaseSet(card_set)
        set_to_id_map[pack_name] = (pack_db_id , pack_release_date)

    print(set_to_id_map["Yu-Gi-Oh! 5D's Tag Force 5 promotional cards"])
    # Yu-Gi-Oh! 5D's Tag Force 5 Promotional Cards
    #create init_cards
    print('Sets Completed')
    response = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php?fname=')
    card_data  =response.json()
    card_to_id_map = {}
    released_card_arr = []

    print(len(card_data['data']))

    for card in card_data['data']:

        if "card_sets" in card: 
            #upload image
            #create card_skeleton
            skeleton_db_id, card_skeleton = createDBcardSkeleton(card)
            card_to_id_map[card_skeleton.yg_pro_id] = (skeleton_db_id, card_skeleton)
            card_release_date = '9999-99-99'
            
            #determine release_date and update
            #create_card_in_set
            for cardSet in card["card_sets"]:    
                try:
                    released_card = CardinSet(
                        card_code = cardSet['set_code'],
                        rarity = cardSet['set_rarity'],
                        card_id = skeleton_db_id,
                        set_id = set_to_id_map[cardSet['set_name']][0]
                    )
                    released_card_arr.append(released_card)
                    card_release_date = min(set_to_id_map[cardSet['set_name']][1], card_release_date)
                except KeyError:
                    logging.warning(f"Card name: {card_skeleton.name} || Card id: {card_skeleton.yg_pro_id} || MissingSetName: {cardSet['set_name']} \n")
                except TypeError as te:
                    logging.warning(f"Card name: {card_skeleton.name} || Card id: {card_skeleton.yg_pro_id} || Error: {te}\n")
            card_skeleton.LegalDate = card_release_date

            #create AltArts
            createDBAltArt(card["card_images"],skeleton_db_id,card_skeleton.yg_pro_id)
    print('Cards Created')
    #Settheinfo on the Cards that are booleans/etc. 
    toggleDBcardSkeletonbools(card_to_id_map)
    
    db.session.add_all(released_card_arr)
    print(len(db.session.new))
    db.session.commit()
    return set_to_id_map , card_to_id_map
    #fill cards

if __name__ == "__main__":  
    with app.app_context():
        set_data, card_data = init_seed_db()
        print('init data_complete')

        with open('Release_set_dict.pkl', 'wb') as f:
            pickle.dump(set_data,f)
        with open('card_dict.pkl', 'wb') as f:
            pickle.dump(card_data, f)
