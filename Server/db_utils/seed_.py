import requests
from helper import createDBReleaseSet , createDBcardSkeleton , createDBAltArt, toggleDBcardSkeletonbools
from config import db
from models import Card , CardinSet 

card_endpoint = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
set_endpoint = 'https://db.ygoprodeck.com/api/v7/cardsets.php'



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
    db.session.commit()

    #create init_cards
    response = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php?fname=')
    card_data  =response.json()
    card_to_id_map = {}
    released_card_arr = []

    for card in card_data['data']:

        if "card_sets" in card: 
            #upload image
            #create card_skeleton
            skeleton_db_id, card_skeleton = createDBcardSkeleton(card)
            card_to_id_map[card_skeleton['ygo_pro_id']] = (skeleton_db_id, card_skeleton)
            card_release_date = '9999-99-99'
            
            #determine release_date and update
            #create_card_in_set
            for cardSet in card["card_sets"]:    
                released_card = CardinSet(
                    card_code = cardSet['set_code'],
                    rarity = cardSet['set_rarity'],
                    card_id = skeleton_db_id,
                    set_id = set_to_id_map[cardSet['set_name']](0)
                )
                released_card_arr.append(released_card)
                card_release_date = min(set_to_id_map[cardSet['set_name']](0), card_release_date)
            
            card_skeleton.LegalDate = card_release_date

            #create AltArts
            createDBAltArt(card["card_images"],skeleton_db_id,card_skeleton.yg_pro_id)
    
    #Settheinfo on the Cards that are booleans/etc. 
    toggleDBcardSkeletonbools()

    #fill cards