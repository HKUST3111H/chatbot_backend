channel_access_token = 'abt2JsNhy4uK+Y0P0eK3Iw7YRr3pL6h3juizwDUUqYXqcPTjeDN59UIPCKhDCPy9W3dfiyx1SymkVcQordtrKlTmuPpSnl3DwcapyMUhlQiQK5FNGMji2UOu4QOGVxdmvD+T+KIB4ebY8pArg/kejQdB04t89/1O/w1cDnyilFU='

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
	try:
		responese = requests.post("https://comp3111h-line-chatbot.herokuapp.com/push", data=post_data)
		responese.raise_for_status()
	except Exception as e:
		print (e)
	return responese

def push_message_to_users(user_ids, message):
	pool = Pool(processes=len(user_ids))
	pool.starmap_async(push_message_to_user, zip(user_ids, repeat(message)), callback=lambda responeses: print (responeses))


line_bot_api = LineBotApi(channel_access_token)

def line_multicast(user_ids, message):
	try:
		line_bot_api.multicast(user_ids, TextSendMessage(text=message))
	except Exception as e:
		print (e)

def line_push(user_id, message):
	try:
		line_bot_api.push_message(user_id, TextSendMessage(text=message))
	except Exception as e:
		print (e)

def line_map_push(user_ids, messages):
	pool = Pool(processes=len(users))
	pool.starmap_async(line_push, zip(user_ids, messages))