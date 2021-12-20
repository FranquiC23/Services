from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm
from .models import Offer, User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username','email', 'user_type','password1' ,'password2']

class MyUserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'last_name', 'username', 'service', 'bio']

class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = "__all__"
        exclude = ['user', 'aspirant', 'status']
