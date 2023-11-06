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
MAX_TAGGED_USERS = 3
MAX_GHOST_FRIENDS = 5
MAX_MEDIADOC_IMAGES = 5

MESSAGE_PARTITIONING = 10
SNAPS_PARTITIONING = 10

names = open('txt/firstnames.txt').read().splitlines()
surnames = open('txt/lastnames.txt').read().splitlines()
words = open('txt/words.txt').read().splitlines()
msg_file = open('txt/messages.txt').read().splitlines()
numbers = open('txt/numbers.txt').read().splitlines()
birthdays = open('txt/birthdays.txt').read().splitlines()
coordinates = open('txt/coordinates.txt').read().splitlines()
streets = open('txt/streets.txt').read().splitlines()

def generate_users():
    
    users_array = []
        
    for i in range(USERS_NUMBER):
        
        hasAvatar = random.choice([True, False])
        
        name = random.choice(names)
        surname = random.choice(surnames)
        
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
                "BusinessLocation": "",
            },
            "nSnaps": random.randint(1, MAX_SNAPS_NUMBERS),
            "ownSnaps": [],
            "LatestOwnSnaps": [],
            "hasAvatar": hasAvatar,
            "Avatar": {
                "idFace": ''.join(random.choices(string.digits, k=5)) if hasAvatar else "",
                "idBody": ''.join(random.choices(string.digits, k=5)) if hasAvatar else "",
                "idShirt": ''.join(random.choices(string.digits, k=5)) if hasAvatar else "",
                "idPants": ''.join(random.choices(string.digits, k=5)) if hasAvatar else "",
                "Timestamp": datetime.datetime.now().timestamp() if hasAvatar else ""
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
                "TagUsers": [],
                "Location": random.choice(["", random.choice(coordinates)]),
                "isPrivate": random.choice([True, False]),
                "Timestamp": datetime.datetime.now().timestamp()
            })
        
    with open('output/snap.json', 'w') as outfile:
        json.dump(snaps_array, outfile, indent=4)
        


def generate_stickers():
    sticker_array = []
    
    user_file = open('output/user.json')
    users_array = json.load(user_file)
    
    username_list = (list(map(lambda x: x["username"], users_array)))
    
    for i in range(MAX_STICKERS_NUMBER):
        sticker_array.append({
            "idSticker": f'Sticker{i}',
            "text": random.choice(words),
            "media": random.choice(["GIF", "animatedSticker", "staticSticker"]),
            "idAvatar": random.choice(username_list), 
            "Timestamp": datetime.datetime.now().timestamp()
        })

    with open('output/sticker.json', 'w') as outfile:
        json.dump(sticker_array, outfile, indent=4)
        
'''def update_stickers():
    
    chat_file = open('output/chat.json')
    chats_array = json.load(chat_file)
    
    sticker_file = open('output/sticker.json')
    stickers_array = json.load(sticker_file)
    
    for chat in chats_array:
        chat_users = set(chat["Users"])
        
        for sticker in stickers_array:
            if sticker["idAvatar"] in chat_users:
                chat["Stickers"].append(sticker)
            
    with open('output/chat.json', 'w') as outfile:
        json.dump(chats_array, outfile, indent=4)'''
        
        
def generate_notify():
    
    user_file = open('output/user.json')
    users_array = json.load(user_file)
    
    notify_array = []
    
    username_list = (list(map(lambda x: x["username"], users_array)))
    
    for user in users_array:
        for i in range(random.randint(0,MAX_NOTIFY_NUMBER)):
            notify_array.append({ 
                "Sender": random.choice(username_list),
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
    
    for notify in notify_array:
        if notify["Cat"] == "Snap":
            notify["Text"] = "New Snap"
            notify["idNotify"] += "Snap"
        elif notify["Cat"] == "Request":
            notify["Text"] = "New Request"
            notify["idNotify"] += "Request"
        elif notify["Cat"] == "Message":
            notify["Text"] = "New Message"
            notify["idNotify"] += "Message"
            
    with open('output/notify.json', 'w') as outfile:
        json.dump(notify_array, outfile, indent=4)
        
    for user in users_array:
        for i in range(random.randint(0,5)):
            user["Notify"].append(random.choice(notify_array))
    
    with open('output/user.json', 'w') as outfile:
        json.dump(users_array, outfile, indent=4)
    

def generate_chats():
    
    user_file = open('output/user.json')
    users_array = json.load(user_file)
    
    usernames = [user["username"] for user in users_array]

    chats = []
    
    chat_count = 100  
    for i in range(chat_count):

        user1, user2 = random.sample(usernames, 2)
        
        chat_id = f'C{i}'
        
        messages = []
        message_count = random.randint(1, 10) 
        for _ in range(message_count):
            sender, receiver = random.choice([user1, user2]), random.choice([user1, user2])
            message = {
                "User": sender,    
                "Text": random.choice(msg_file),
                "Timestamp": datetime.datetime.now().timestamp()
            }
            messages.append(message)

        last_message_timestamp = max(message["Timestamp"] for message in messages)

        chat = {
            "idChat": chat_id,
            "Media": {
                "Pics": [],
                "Docs": []
            },
            "Users": [user1, user2],
            "Messages": messages,
            "Stickers": [],
            "Timestamp": last_message_timestamp
        }

        chats.append(chat)

            
    with open('output/chat.json', 'w') as chat_file:
        json.dump(chats, chat_file, indent=4)
    

    
def update_chats():
    
    chat_file = open('output/chat.json')
    chats_array = json.load(chat_file)
    
    sticker_file = open('output/sticker.json')
    stickers_array = json.load(sticker_file)
    
    for chat in chats_array:
        chat_users = set(chat["Users"])
        
        for sticker in stickers_array:
            if sticker["idAvatar"] in chat_users:
                chat["Stickers"].append(sticker)
   
    for chats in chats_array:
        for i in range(random.randint(0,MAX_MEDIADOC_IMAGES)):
            chats["Media"]["Pics"].append((f"pic{i}"))
            chats["Media"]["Docs"].append((f"doc{i}"))
            
    with open('output/chat.json', 'w') as outfile:
        json.dump(chats_array, outfile, indent=4)

        
def update_users():
    
    user_file = open('output/user.json')
    users_array = json.load(user_file)
    
    # AGGIUNTA FRIENDS
    for user in users_array:
        for i in range(random.randint(1,MAX_FRIENDS_NUMBER)):
            
            username_list = (list(map(lambda x: x["username"], users_array)))
            sub_list = user["Friends"] + [user["username"]]
            username_list = list(set(username_list) - set(sub_list))
            
            rand_user = random.choice(username_list)
            user["Friends"].append(rand_user)
            if (random.choice([True,False])): user["CloseFriends"].append(rand_user)
            
    # AGGIUNTA BLOCKED
    for user in users_array:
        for i in range(random.randint(1,MAX_BLOCKED_NUMBER)):
            
            username_list = (list(map(lambda x: x["username"], users_array)))
            sub_list = user["Friends"] + [user["username"]]
            username_list = list(set(username_list) - set(sub_list))
            
            rand_user = random.choice(username_list)
            user["Blocked"].append(rand_user)
                        
                
    snap_file = open('output/snap.json')
    snaps_array = json.load(snap_file)
    
    # AGGIUNTA NUMERO SNAP PER UTENTE
    for user in users_array:
        filtered_snaps = list(filter(lambda x: x["ownSnaps"] == user["username"], snaps_array))
        filtered_snaps.sort(key = lambda x: x["Timestamp"], reverse=False)
        filtered_snaps = list(map(lambda x: x["idSnap"], filtered_snaps))
        user["LatestOwnSnaps"] = filtered_snaps[-SNAPS_PARTITIONING:]
        
        for snap in snaps_array:
            if snap["ownSnaps"] == user["username"]:
                user["ownSnaps"].append(snap["idSnap"])
                
    with open('output/user.json', 'w') as outfile:
        json.dump(users_array, outfile, indent=4)
    
    # AGGIUNTA MAPS CON GHOSTFRIENDS
    maps_array = []

    for user in users_array:
        
        friends_list = list(set(user["Friends"]))    
             
        if len(friends_list) == 0:
            is_ghost_mode = False
            ghost_friends_list = []
        else:
            is_ghost_mode = random.choice([True, False])
            if is_ghost_mode == True:
                ghost_friends_list = random.choices(friends_list, k=random.randint(1,MAX_GHOST_FRIENDS))
            else:
                ghost_friends_list = []    
                
        maps_array.append({
            "idAsset": ''.join(random.choices(string.digits, k=6)),
            "User": user["username"],
            "Snaps": [],
            "StatusGPS": random.choice([True, False]),
            "isHotspot": random.choice([True, False]),
            "isSatellite": random.choice([True, False]),
            "isHideLiveLocation": random.choice([True, False]),
            "GhostMode": {
                "isGhostMode": is_ghost_mode,
                "GhostModeFriends": ghost_friends_list,
            }
        })

    with open('output/map.json', 'w') as outfile:
        json.dump(maps_array, outfile, indent=4)

def update_snaps():
   
    user_file = open('output/user.json')
    users_array = json.load(user_file)

    snap_file = open('output/snap.json')
    snaps_array = json.load(snap_file)

    username_list = (list(map(lambda x: x["username"], users_array)))
    
    # AGGIUNTA TAGGED USERS E LIKES
    for snap in snaps_array:
        for i in range(snap["LikesCount"]):
            snap["UserLikes"].append(random.choice(list(set(username_list)-set(snap["UserLikes"]))))
        for i in range(random.randint(0,MAX_TAGGED_USERS)):
            snap["TagUsers"].append(random.choice(list(set(username_list)-set(snap["TagUsers"]))))
    
    with open('output/snap.json', 'w') as outfile:
        json.dump(snaps_array, outfile, indent=4)
    
def update_business():
    
    user_file = open('output/user.json')
    users_array = json.load(user_file)
    
    for i in range(USERS_NUMBER):
        if users_array[i]["BusinessInfo"]["isBusiness"]:
            users_array[i]["BusinessInfo"]["BusinessName"] = f"UserBusiness{i}"
            users_array[i]["BusinessInfo"]["BusinessAddress"] = f"{random.choice(streets)}, n. {random.randint(1,100)}"
            users_array[i]["BusinessInfo"]["BusinessLocation"] = random.choice(coordinates)
                
    with open('output/user.json', 'w') as outfile:
        json.dump(users_array, outfile, indent=4)


def update_maps():
    
    snap_file = open('output/snap.json')
    snaps_array = json.load(snap_file)
    
    maps_file = open('output/map.json')
    maps_array = json.load(maps_file)
    
    user_file = open('output/user.json')
    users_array = json.load(user_file)
        
    for snap in snaps_array:
        for maps in maps_array:
            if snap["Location"] and snap["ownSnaps"] == maps["User"]:
                maps["Snaps"].append(snap["idSnap"])
            
    with open('output/map.json', 'w') as outfile:
        json.dump(maps_array, outfile, indent=4)
            
if __name__ == '__main__':
    generate_users()
    generate_snaps()
    generate_chats()
    generate_stickers() 
    generate_notify()
    
    update_users()
    update_business()
    update_snaps()
    update_chats()
    #update_stickers()
    update_notify()
    update_maps()