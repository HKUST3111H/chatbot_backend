
from django import forms
from .models import *

class MessageForm(forms.Form):
	users = forms.ModelMultipleChoiceField(queryset=User.objects.all())
	message = forms.CharField(label='Push Message', max_length=100)
