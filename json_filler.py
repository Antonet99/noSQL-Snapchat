import random
import json
import datetime
import string


USERS_NUMBER = 100
MAX_SNAPS_NUMBERS = 15
STICKERS_NUMBER = 1000

DIRECT_PARTITIONING = 10

names = open('names.txt').read().splitlines()
words = open('words.txt').read().splitlines()
msgs = open('msg.txt').read().splitlines()

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
            "nSnaps": random.randint(1, MAX_SNAPS_NUMBERS),
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
        
def generate_snaps():
    
    user_file = open('output/user.json')
    users_array = json.load(user_file)
    
    snaps_array = []
    for user in users_array:
        for i in range(user["nSnaps"]):
            snaps_array.append({
                "idSnap": f'{user["username"]}Snap{i}',
                "media": {
                    "text": random.choice(words),
                    "pic": "",
                    "music": ""
                    },
                "ownSnap": user["username"],
                "UserLikes": [],
                "Location": "",
                "LikesCount": random.randint(0, USERS_NUMBER),
                "isPrivate": random.choice([True, False]),
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
    with open('output/snap.json', 'w') as outfile:
        json.dump(snaps_array, outfile, indent=4)
        
        
def generate_chats():
    chats_array = []
    for i in range(random.randint(0,USERS_NUMBER*5)):
        chats_array.append({
            "idChat": f"C{i}",
            "Media": [],
	        "Users": [],
	        "Messages": [],
            "Timestamp": ""
        })

    with open('output/chat.json', 'w') as outfile:
        json.dump(chats_array, outfile, indent=4)
        
def generate_messages():

    message = random.choice(msgs)
    chat_file = open('output/chat.json')
    chats_array = json.load(chat_file)

    idChat_list = list(map(lambda x: x["idChat"], chats_array))

    messages_array = []
    for i in range(random.randint(0,USERS_NUMBER*50)):
        messages_array({
            "idMsg": f"msg{i}",
            "content": {
                "text": random.choice(message), 
                "timestamp": datetime.datetime.now().timestamp()
            },
            "idChat": random.choice(idChat_list),
        })

    with open('output/messages.json', 'w') as outfile:
        json.dump(messages_array, outfile, indent=4)


def generate_stickers():
    sticker_array = []
    for i in range(STICKERS_NUMBER):
        sticker_array.append({
            "idSticker": f'Sticker{i}',
            "text": random.choice(words),
            "media": "",
            "idAvatar": random.randint(0,USERS_NUMBER),
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    with open('output/sticker.json', 'w') as outfile:
        json.dump(sticker_array, outfile, indent=4)
        
def update_chats():
    
    chat_file = open('output/chat.json')
    chats_array = json.load(chat_file)
    
    user_file = open('output/user.json')
    users_array = json.load(user_file)
    
    direct_file = open('output/direct.json')
    directs_array = json.load(direct_file)
    
    username_list = (list(map(lambda x: x['username'], users_array)))
    
    for chat in chats_array:
        for i in range(2):
            chat['Users'].append(random.choice(list(set(username_list) - set(chat['Users']))))
    
        filtered_directs = list(filter(lambda x: x["idChat"] == chat["idChat"], directs_array))
        filtered_directs.sort(key = lambda x: x["content"]["timestamp"], reverse=False)
        chat["Messages"] = filtered_directs[:DIRECT_PARTITIONING-1]
    
        chat["Timestamp"] = chat["Messages"][-1]["content"]["timestamp"]
        
        
    with open('output/chat.json', 'w') as outfile:
        json.dump(chats_array, outfile, indent=4)
    
    with open('output/direct.json', 'w') as outfile:
        json.dump(directs_array, outfile, indent=4)
    
            
if __name__ == '__main__':
    generate_users()
    generate_stickers()
    generate_snaps()
    generate_chats()
    generate_messages()
    update_chats()