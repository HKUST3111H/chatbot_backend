
from django import forms
from .models import *
from material import *

class MessageForm(forms.Form):
	users = forms.ModelMultipleChoiceField(queryset=User.objects.all())
	message = forms.CharField(label='Push Message', max_length=100)
	layout = Layout(
		Fieldset('Receivers', Row('users')),
		Fieldset('Message', Row('message')))