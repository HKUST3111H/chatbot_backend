
import requests
from itertools import repeat
from .models import *
from .forms import *
from multiprocessing import Process, Pool

def push_message_to_user(user, message):
	post_data = {'receiver': user.id, 'message': message+user.name}
	post_data['receiver'] = "Ufedbdb7c3d944c326a4251ac135b69e3"
	try:
		responese = requests.post("https://gentle-fjord-43717.herokuapp.com/push", data=post_data)
		responese.raise_for_status()
	except Exception as e:
		print (e)
	return responese

def push_message_to_users(users, message):
	pool = Pool(processes=len(users))
	pool.starmap_async(push_message_to_user, zip(users, repeat(message)), callback=lambda responeses: print (responeses))

