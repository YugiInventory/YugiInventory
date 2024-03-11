import requests
from app import app
from models import * 

#Fill the database with card information

# https://db.ygoprodeck.com/api/v7/cardinfo.php has all the card information 

#Card_Sets has information on the set namde, code, rarity, 

#We fill out information on the ReleaseSets, Cards, CardsinSets


card_endpoint = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
set_endpoint = 'https://db.ygoprodeck.com/api/v7/cardsets.php'

set_to_id_map = {} 

def get_release_sets():
    response = requests.get(set_endpoint)
    sets_info = response.json()
    outlist = []
    error_list = []
    #Since we are seeding with an empty db we can assume its all incrementing from 0. In that case instead of checking for the existance of the value in the database constantly we can assume it will be uploaded in the same order as we go through the set info and create a dictionary (set to id map) that we can use to refer to what the primary key. This would only work when the database is created for the first time. 

    j = 0 
    for card_set in sets_info:
        print(card_set)
        try:
            pack = ReleaseSet(
                name = card_set['set_name'],
                releaseDate = card_set.get('tcg_date', None),
                card_count = card_set['num_of_cards'],
                set_code = card_set['set_code']
            )
            j+=1 
            set_to_id_map[card_set['set_name']] = j
        except:
            error_list.append(card_set)
        outlist.append(pack)
    
    print(error_list)
    return outlist


if __name__ == "__main__":
    with app.app_context():
        releaseSet_info = get_release_sets()
        db.session.add_all(releaseSet_info)
        db.session.commit()