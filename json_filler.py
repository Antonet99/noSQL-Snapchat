import random
import json
import datetime
import string


USERS_NUMBER = 100
MAX_SNAPS_NUMBERS = 10
STICKERS_NUMBER = 1000

names = open('names.txt').read().splitlines()
words = open('words.txt').read().splitlines()

def generate_users():
    users_array = []
    for i in range(USERS_NUMBER):
        name = random.choice(names)
        users_array.append({
            "username": f"User{i}",
            "Anagrafica": {
                "FirstName": name,
                "LastName": random.choice(names), #da rimuovere
                "email": f"{name}.{i}@email.com",
                "snapCode": ''.join(random.choices(string.digits, k=8)),
                "password": f"password_{name}",
                "genre": random.choice(["male", "female", "other"]),
                "phoneNumber": "",
                "birthday": ""
            },
            "BusinessInfo": {
                "isBusiness": random.choice([True, False]),
                "BusinessImage": "",
                "BusinessName": "",
                "BusinessAddress": "",
            },
            "nSnaps": random.randint(0, MAX_SNAPS_NUMBERS),
            "ownSnaps": [],
            "LatestOwnSnaps": [],
            "hasAvatar": random.choice([True, False]),
            "Notify": [],
            "Friends": [],
            "CloseFriends": [],
            "Followed": [],
            "Blocked": []
        }) 
        
    with open('output/user.json', 'w') as outfile:
        json.dump(users_array, outfile, indent=4)


def generate_stickers():
    sticker_array = []
    for i in range(STICKERS_NUMBER):
        sticker_array.append({
            "idSticker": f'Sticker{i}',
            "text": random.choice(words),
            "media": "",
            "idAvatar": random.randint(0,USERS_NUMBER),
        })

    with open('output/sticker.json', 'w') as outfile:
        json.dump(sticker_array, outfile, indent=4)
        
if __name__ == '__main__':
    generate_users()
    generate_stickers()