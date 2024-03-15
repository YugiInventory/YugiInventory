import requests
from app import app
from models import * 
from tempfile import NamedTemporaryFile
import boto3

#Fill the database with card information

# https://db.ygoprodeck.com/api/v7/cardinfo.php has all the card information 

#Card_Sets has information on the set namde, code, rarity, 

#We fill out information on the ReleaseSets, Cards, CardsinSets

session = boto3.Session(profile_name='shamsk')
s3 = session.client('s3')

card_endpoint = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
set_endpoint = 'https://db.ygoprodeck.com/api/v7/cardsets.php'

set_to_id_map = {} 
card_to_id_map = {}
failed_cards = []

def get_release_sets():
    response = requests.get(set_endpoint)
    sets_info = response.json()
    outlist = []
    error_list = []
    #Since we are seeding with an empty db we can assume its all incrementing from 0. In that case instead of checking for the existance of the value in the database constantly we can assume it will be uploaded in the same order as we go through the set info and create a dictionary (set to id map) that we can use to refer to what the primary key. This would only work when the database is created for the first time. 

    j = 0 
    for card_set in sets_info:
        # print(card_set)
        try:
            pack = ReleaseSet(
                name = card_set['set_name'],
                releaseDate = card_set.get('tcg_date', None),
                card_count = card_set['num_of_cards'],
                set_code = card_set['set_code']
            )
            j+=1 
            set_to_id_map[card_set['set_name']] = j
            outlist.append(pack)
        except:
            error_list.append(card_set)
    return outlist

#A couple ideas for seeding the card data. All cards will have the following parameters: id, name, type, frameType, desc
#Monster cards have an atk, def, level, race, attribute
#Spell/Trap cards have a race
#Pendulums have a scale

#We have other ways to check for boolean values from different end points and we can use those to modify the values before submitting to the db. 

def getinitcards():
    response = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php?fname=nekroz')
    card_data = response.json()

    for card in card_data['data']:

        #create the image and upload it to s3
        #then create the skeleton object and add it to my dictionary of cards

        if "card_sets" in card: #Card has a tcg printing not an anime/namga card

            card_id = card['id']
            img_url = card['card_images'][0]['image_url_small']
            
            
            #image upload section
            bucket_name = 'yugitorybuckettest'
            s3_key = f'{card_id}.jpg'
            s3_url = f'https://{bucket_name}.s3.amazonaws.com/{s3_key}' 

            img_bin = requests.get(img_url).content

            with NamedTemporaryFile(suffix="'jpg") as temp_file:
                temp_file.write(img_bin)
                file_name=temp_file.name
                # s3.upload_file(file_name,bucket_name,s3_key)

            #create the card 
            try:
                init_card = Card(
                    yg_pro_id = card_id,
                    name = card['name'],
                    description = card['desc'],
                    attack = None,
                    defense = None,
                    level = None,
                    isEffect = None,
                    isTuner = None,
                    isFlip = None,
                    isSpirit = None,
                    isUnion = None,
                    isGemini = None,
                    isPendulum = None,
                    isRitual = None,
                    isToon = None,
                    isFusion = None,
                    isSynchro = None,
                    isXYZ = None,
                    isLink = None,
                    card_type = None,
                    card_race = None,
                    card_attribute = None,
                    LegalDate = None,
                    card_image = s3_url,
                    frameType = card['frameType']
                )        
                card_to_id_map[card_id] = init_card
            except:
                #failed to create the card
                failed_cards.append(card_id)
        else:
            continue

        # # with open('temp_fors3.jpg', 'wb') as file:
        # #     file.write(img_bin)

        # # file_name = '/home/shams/Development/code/post-grad/Yugi_Inventory/YugiInventory/Server/temp_fors3.jpg'
        # bucket_name = 'yugitorybuckettest'
        # s3_key = f'{card_id}.jpg'
        # s3.upload_file(file_name,bucket_name,s3_key)
        # s3_url = f'https://{bucket_name}.s3.amazonaws.com/{s3_key}' 

    print(card_to_id_map)
    print(failed_cards)

if __name__ == "__main__":
    with app.app_context():
        # releaseSet_info = get_release_sets()
        # db.session.add_all(releaseSet_info)
        # db.session.commit()
        getinitcards()
        print('seeding complete')