channel_access_token = 'KNRFob43cptjHSZ3kfgqkb5MgDDXbtkhJDQDl5au0pq9c4oeitMXYAoK4wRd/jDu+NJv48dAQCdSOgLWQwOMC1B50j6REkm26uuuomB2ttARfWRiAOSrLz11GP3FGSloVpRbxl8T8he8egLU7XSiewdB04t89/1O/w1cDnyilFU='

import requests
from itertools import repeat
from .models import *
from .forms import *
from multiprocessing import Process, Pool

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

def push_message_to_user(user, message):
	post_data = {'receiver': user.id, 'message': message+user.name}
	post_data['receiver'] = "Ufedbdb7c3d944c326a4251ac135b69e3"
	try:
		responese = requests.post("https://gentle-fjord-43717.herokuapp.com/push", data=post_data)
		responese.raise_for_status()
	except Exception as e:
		print (e)
	return responese

def push_message_to_users(user_ids, message):
	pool = Pool(processes=len(user_ids))
	pool.starmap_async(push_message_to_user, zip(user_ids, repeat(message)), callback=lambda responeses: print (responeses))


line_bot_api = LineBotApi(channel_access_token)

def line_multicast(user_ids, message):
	user_ids = ['Ufedbdb7c3d944c326a4251ac135b69e3']
	line_bot_api.multicast(user_ids, TextSendMessage(text=message))

def line_push(user_id, message):
	line_bot_api.push(user_id, message)

def line_map_push(user_ids, messages):
	pool = Pool(processes=len(users))
	pool.starmap_async(line_push, zip(user_ids, messages))