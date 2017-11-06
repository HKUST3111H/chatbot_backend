
from django import forms
from .models import *

class MessageForm(forms.Form):
	message = forms.CharField(label='Push Message', max_length=100)
	