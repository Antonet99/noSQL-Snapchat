import random
import json
import datetime
import string


USERS_NUMBER = 100
MAX_SNAPS_NUMBERS = 30
MAX_FRIENDS_NUMBER = 30
MAX_BLOCKED_NUMBER = 10
MAX_STICKERS_NUMBER = 100
MAX_NOTIFY_NUMBER = 10

MESSAGE_PARTITIONING = 10
SNAPS_PARTITIONING = 10

names = open('txt/firstnames.txt').read().splitlines()
surnames = open('txt/lastnames.txt').read().splitlines()
words = open('txt/words.txt').read().splitlines()
messages = open('txt/messages.txt').read().splitlines()
numbers = open('txt/numbers.txt').read().splitlines()
birthdays = open('txt/birthdays.txt').read().splitlines()
coordinates = open('txt/coordinates.txt').read().splitlines()

def generate_users():
    
    name = random.choice(names)
    surname = random.choice(surnames)
    
    users_array = []
    
    for i in range(USERS_NUMBER):
        users_array.append({
            "username": f"User{i}",
            "Anagrafica": {
                "FirstName": name,
                "LastName": surname,
                "email": f"{name}.{surname}.{i}@email.com",
                "snapCode": ''.join(random.choices(string.digits, k=8)),
                "password": f"password_{name}",
                "genre": random.choice(["male", "female", "other"]),
                "phoneNumber": random.choice(numbers),
                "birthday": random.choice(birthdays),
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
            "Avatar": {
                "idFace": ''.join(random.choices(string.digits, k=5)),
                "idBody": ''.join(random.choices(string.digits, k=5)),
                "idShirt": ''.join(random.choices(string.digits, k=5)),
                "idPants": ''.join(random.choices(string.digits, k=5)),
                "Timestamp": datetime.datetime.now().timestamp()
            },
            "Notify": [],
            "Friends": [],
            "CloseFriends": [],
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
                "ownSnaps": user["username"],
                "UserLikes": [],
                "LikesCount": random.randint(0, USERS_NUMBER),
                "Location": random.choice(coordinates),
                "isPrivate": random.choice([True, False]),
                "Timestamp": datetime.datetime.now().timestamp()
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

    chat_file = open('output/chat.json')
    chats_array = json.load(chat_file)

    idChat_list = list(map(lambda x: x["idChat"], chats_array))

    messages_array = []
    for i in range(random.randint(0,USERS_NUMBER*50)):
        messages_array.append({
            "idMsg": f"msg{i}",
            "content": {
                "text": random.choice(messages),
                "timestamp": datetime.datetime.now().timestamp()
            },
            "idChat": random.choice(idChat_list),
        })

    with open('output/message.json', 'w') as outfile:
        json.dump(messages_array, outfile, indent=4)


def generate_stickers():
    sticker_array = []
    
    user_file = open('output/user.json')
    users_array = json.load(user_file)
    
    username_list = (list(map(lambda x: x["username"], users_array)))
    
    for i in range(MAX_STICKERS_NUMBER):
        sticker_array.append({
            "idSticker": f'Sticker{i}',
            "text": random.choice(words),
            "media": "",
            "idAvatar": random.choice(username_list), #inserire chiave user casuale 
            "Timestamp": datetime.datetime.now().timestamp()
        })

    with open('output/sticker.json', 'w') as outfile:
        json.dump(sticker_array, outfile, indent=4)
        
        
def generate_notify():
    
    user_file = open('output/user.json')
    users_array = json.load(user_file)
    
    notify_array = []
    
    for user in users_array:
        for i in range(random.randint(0,MAX_NOTIFY_NUMBER)):
            notify_array.append({ 
                "Receiver": user["username"],
                "idNotify": f'Notify{i}',
                "Cat": random.choice(["Snap", "Request", "Message"]),
                "Text": ""
            })

    with open('output/notify.json', 'w') as outfile:
        json.dump(notify_array, outfile, indent=4)
        
        
def update_notify():
    
    user_file = open('output/user.json')
    users_array = json.load(user_file)
    
    notify_file = open('output/notify.json')
    notify_array = json.load(notify_file)
    
    username_list = (list(map(lambda x: x["username"], users_array)))
    
    #inserimento in ogni utente tutte le notifiche all'interno di notify_array che hanno receiver = user["username"]
    for user in users_array:
        filtered_notify = list(filter(lambda x: x["Receiver"] == user["username"], notify_array))
        filtered_notify = list(map(lambda x: x["idNotify"], filtered_notify))
        user["Notify"] = filtered_notify
    
    with open('output/user.json', 'w') as outfile:
        json.dump(users_array, outfile, indent=4)
    
    
def update_chats():
    
    chat_file = open('output/chat.json')
    chats_array = json.load(chat_file)
    
    user_file = open('output/user.json')
    users_array = json.load(user_file)
    
    message_file = open('output/message.json')
    messages_array = json.load(message_file)
    
    username_list = (list(map(lambda x: x['username'], users_array)))
    
    for chat in chats_array:
        for i in range(2):
            chat['Users'].append(random.choice(list(set(username_list) - set(chat['Users']))))
    
        filtered_directs = list(filter(lambda x: x["idChat"] == chat["idChat"], messages_array))
        filtered_directs.sort(key = lambda x: x["content"]["timestamp"], reverse=False)
        chat["Messages"] = filtered_directs[:MESSAGE_PARTITIONING-1]
    
        chat["Timestamp"] = chat["Messages"][-1]["content"]["timestamp"]
        
        
    with open('output/chat.json', 'w') as outfile:
        json.dump(chats_array, outfile, indent=4)
    
    with open('output/message.json', 'w') as outfile:
        json.dump(messages_array, outfile, indent=4)
        
def update_users():
    
    user_file = open('output/user.json')
    users_array = json.load(user_file)
    
    for user in users_array:
        for i in range(random.randint(1,MAX_FRIENDS_NUMBER)):
            
            username_list = (list(map(lambda x: x["username"], users_array)))
            sub_list = user["Friends"] + [user["username"]]
            username_list = list(set(username_list) - set(sub_list))
            
            rand_user = random.choice(username_list)
            user["Friends"].append(rand_user)
            if (random.choice([True,False])): user["CloseFriends"].append(rand_user)
    
    for user in users_array:
        for i in range(random.randint(1,MAX_BLOCKED_NUMBER)):
            
            username_list = (list(map(lambda x: x["username"], users_array)))
            sub_list = user["Friends"] + [user["username"]]
            username_list = list(set(username_list) - set(sub_list))
            
            rand_user = random.choice(username_list)
            user["Blocked"].append(rand_user)
            
                
    snap_file = open('output/snap.json')
    snaps_array = json.load(snap_file)
    
    for user in users_array:
        filtered_snaps = list(filter(lambda x: x["ownSnaps"] == user["username"], snaps_array))
        filtered_snaps.sort(key = lambda x: x["Timestamp"], reverse=False)
        filtered_snaps = list(map(lambda x: x["idSnap"], filtered_snaps))
        user["LatestOwnSnaps"] = filtered_snaps[:SNAPS_PARTITIONING-1]
        
        for snap in snaps_array:
            if snap["ownSnaps"] == user["username"]:
                user["ownSnaps"].append(snap["idSnap"])
                
    with open('output/user.json', 'w') as outfile:
        json.dump(users_array, outfile, indent=4)

def update_snaps():
   
    user_file = open('output/user.json')
    users_array = json.load(user_file)

    snap_file = open('output/snap.json')
    snaps_array = json.load(snap_file)

    username_list = (list(map(lambda x: x["username"], users_array)))
    for snap in snaps_array:
        for i in range(snap["LikesCount"]):
            snap["UserLikes"].append(random.choice(list(set(username_list)-set(snap["UserLikes"]))))
    
    with open('output/snap.json', 'w') as outfile:
        json.dump(snaps_array, outfile, indent=4)
    
def update_business():
    
    user_file = open('output/user.json')
    users_array = json.load(user_file)
    
    for i in range(USERS_NUMBER):
        if users_array[i]["BusinessInfo"]["isBusiness"]:
            users_array[i]["BusinessInfo"]["BusinessName"] = f"UserBusiness{i}"
                
    with open('output/user.json', 'w') as outfile:
        json.dump(users_array, outfile, indent=4)
            
if __name__ == '__main__':
    generate_users()
    generate_stickers()
    generate_snaps()
    generate_chats()
    generate_messages()
    generate_notify()
    generate_stickers()
    
    update_chats()
    update_users()
    update_snaps()
    update_business()
    update_notify()