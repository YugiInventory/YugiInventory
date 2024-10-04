import requests
import time
import boto3
from app import app
from config import db
from models import *
from sqlalchemy import text
from tempfile import NamedTemporaryFile


#Helper Functions

#testing imports
from Server.db_utils.testingfunctions import deleteSet

from DB_modification_functions import createDBCard, createDBCardinSet , createDBReleaseSet

#Update Database functions

card_endpoint = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'
set_endpoint = 'https://db.ygoprodeck.com/api/v7/cardsets.php'
release_set_endpoint = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?cardset='

def createDBReleaseSet(release_set): #releaseSet is the API object
        pack = ReleaseSet(
            name = release_set['set_name'],
            releaseDate = release_set.get('tcg_date', None),
            card_count = release_set['num_of_cards'],
            set_code = release_set['set_code']
        )
        # with app.app_context():
        db.session.add(pack)
        db.session.flush()
        return pack.id , pack.name , pack.releaseDate

def upload_images(img_url,id): #imgURL is the ygoAPI link to the image, id is the ygproid from the API
    session = boto3.Session(profile_name='shamsk')
    s3 = session.client('s3')
    bucket_name = 'yugitorybuckettest'
    s3_key = f'{id}.jpg'
    s3_url = f'https://{bucket_name}.s3.amazonaws.com/{s3_key}' 
    retries = 0 

    while retries < 3: 
        try:
            img_bin = requests.get(img_url).content
            with NamedTemporaryFile(suffix="'jpg") as temp_file:
                temp_file.write(img_bin)
                file_name=temp_file.name
                s3.upload_file(file_name,bucket_name,s3_key)
            break
        
        except Exception as e:
            retries +=1 
            if retries == 3:
                print(f'Error getting image for id {id} Error :{e}')
                break
            print(f'Error: Retrying attepmt {retries}')        
        time.sleep(60)

    return s3_url

def createDBcardSkeleton(card_obj):
    primary_id = card_obj['id']
    img_url = card_obj['card_images'][0]['image_url_small']

    card_type = 'Monster'
    if 'Spell' in card_obj['type']:
        card_type = 'Spell'
    elif 'Trap' in card_obj['type']:
        card_type = 'Trap'

    s3_url = 'temp' #upload_images(img_url=img_url,id=card_id)

    card_skeleton = Card(
        yg_pro_id = primary_id,
        name = card_obj['name'],
        description = card_obj['desc'],
        attack = card_obj.get('atk'), #card['atk'] if card['atk'] else None,
        defense = card_obj.get('def'), #card['def'] if card['def'] else None,
        level = card_obj.get('level'), #card['level'] if card['level'] else None,
        isEffect = False,
        isTuner = False,
        isFlip = False,
        isSpirit = False,
        isUnion = False,
        isGemini = False,
        isPendulum = False,
        isRitual = False,
        isToon = False,
        isFusion = False,
        isSynchro = False,
        isXYZ = False,
        isLink = False,
        card_type = card_type,
        card_race = card_obj.get('race'), #card['race'] if card['race'] else None,
        card_attribute = card_obj.get('attribute'), #card['attribute'] if card['attribute'] else None,
        LegalDate = None,
        card_image = s3_url,
        frameType = card_obj['frameType']
    ) 
    db.session.add(card_skeleton)
    db.session.flush()

    return card_skeleton.id , card_skeleton

def createDBAltArt(card_images_arr,card_id,default_id):
    #logic to to create Alts if needed
    if len(card_images_arr) > 1:
        for alt_art in card_images_arr:
            if alt_art["id"] != default_id:
                s3_url = upload_images(alt_art["image_url_small"],alt_art["id"])
                new_alt_art = AltArt(
                    card_id = card_id,
                    card_image = s3_url,
                    ygopro_id = alt_art["id"]
                )
                db.session.add(new_alt_art)
    return

def toggleDBcardSkeletonbools(init_cards):
    #fill out the information in the Cards thar are None
    #We can have the enpoint we are searching for and the values to toggle on 

    type_endpoint_dict = {
        "Effect Monster" : ['isEffect'],
        "Flip Effect Monster" : ['isFlip', 'isEffect'],
        "Gemini Monster" : ['isGemini'], 
        "Normal Tuner Monster" : ['isTuner'],
        "Pendulum Effect Monster" : ['isEffect','isPendulum'], 
        "Pendulum Flip Effect Monster" : ['isEffect','isFlip','isPendulum'], 
        "Pendulum Normal Monster" : ['isPendulum'], 
        "Pendulum Tuner Effect Monster" : ['isPendulum','isTuner','isEffect'], 
        "Ritual Effect Monster" : ['isRitual', 'isEffect'],
        "Ritual Monster" : ['isRitual'],
        "Spirit Monster" : ['isSpirit'],
        "Toon Monster" : ['isToon'],
        "Tuner Monster" : ['isTuner'],
        "Union Effect Monster" : ['isUnion'], 
        "Fusion Monster" : ['isFusion'],
        "Link Monster" : ['isLink'],
        "Pendulum Effect Fusion Monster" : ['isPendulum','isFusion','isEffect'],
        "Synchro Monster" : ['isSynchro'], 
        "Synchro Pendulum Effect Monster" : ['isSynchro','isPendulum','isEffect'],
        "Synchro Tuner Monster" : ['isSynchro','isTuner'],
        "XYZ Monster" : ['isXYZ'],
        "XYZ Pendulum Effect Monster" : ['isXYZ','isPendulum','isEffect']
    }
    
    base_url = 'https://db.ygoprodeck.com/api/v7/cardinfo.php?type='

    print('Adding Toggles')

    for key in type_endpoint_dict: #type_endpoint_dict
        #get the api results
        #search for the cards and the flip the toggle
        i = 0 
        toggles = type_endpoint_dict[key]
        req_url = base_url + key

        req_info = requests.get(req_url)
        card_data = req_info.json()
        print(f'Current Key {key}')
        total_entries = len(card_data['data'])

        for card in card_data['data']:
            if init_cards.get(card['id']):
                i+=1
                card_info = init_cards[card['id']]
                #update card toggles
                for toggle in toggles:
                    setattr(card_info, toggle , True)
                #update dict
                init_cards[card['id']] = card_info
                print(f'{i} of {total_entries}')
    cards_array = list(init_cards.values())

    return cards_array , init_cards





def update_database():
#First we want to figure out which releaseSets we do not have in the database. 
#We can then go through the releasesets individual cards.
#If that card already exists, then we will create new cardinSets entry. 
#If that card doesn't exist, then we will create a new card entry. We will also create a new cardinSets entry. 
#New cards would also need to be created on S3. 
#afaik all cards are released in new sets or promotions etc. Can i query for cards by a release set? i think i should be able 
    release_sets = getApiReleaseSets()    
    saved_sets = getDBReleaseSets()
    update_list = reconcileReleaseSets(release_sets, saved_sets)
    for record in update_list: #iterate over the list of sets we do not have
        out = createDBReleaseSet(record) #create the record if success returns id and name
        #get a list of cards from the set
        
        if isinstance(out,tuple):
            set_id = out[0]
            set_name = out[1]
            response = requests.get(release_set_endpoint + set_name,timeout=30.0)
            cardsinSet_List = response.json()
            for card in cardsinSet_List['data']: #Go through the cards in each set
                #check if we have the card
                card_exists = Card.query.filter(Card.name==str(card['name'])).first()
                try:
                    if card_exists:
                        createDBCardinSet(set_id,card_exists.id,set_name,card)
                    else:
                        card_id = createDBCard(card)  #Returns the id for the new card. 
                        createDBCardinSet(set_id, card_id, set_name,card)
                except:
                    return
            db.session.commit()    
        #If we put together a full releaseSet with no errors we can commit that to the db. 
        else:
            #Error We didnt create a sucessfull record
            return
        
def getApiReleaseSets():
    response = requests.get(set_endpoint)
    allSets = response.json()
    setlist = []
    for releaseset in allSets:
        setlist.append(releaseset) 
    return setlist

def getDBReleaseSets():
    setdict = {}
    with app.app_context():
        release_list = ReleaseSet.query.all()
        for set in release_list:
            setdict[set.name] = set.id
    return setdict

def reconcileReleaseSets(setlist, setdict): #given a list of entries see if they are in out database(db is the setdict for id access and faster lookup)
    unadded_sets = []
    for releaseSet in setlist:
        if releaseSet['set_name'] not in setdict:
            unadded_sets.append(releaseSet)
    return unadded_sets

if __name__ == "__main__":

    with app.app_context():
        deleteSet('Absolute Powerforce')
        deleteSet('Abyss Rising')
        update_database()












