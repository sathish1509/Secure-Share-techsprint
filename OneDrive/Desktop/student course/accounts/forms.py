from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'receive_notifications', 'date_of_birth')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'receive_notifications', 'bio', 'profile_picture', 'date_of_birth')

class NotificationPreferenceForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('receive_notifications',)
        labels = {
            'receive_notifications': 'Would you like to receive course notifications?'
        } 