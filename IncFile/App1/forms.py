from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
    max_length=30,
    required=True,
    widget=forms.TextInput(attrs={ 'style': 'height: 30px; font-size: 16px;width:250px ' 
                                  })
    )

    last_name = forms.CharField(
    max_length=30,
    required=True,
    widget=forms.TextInput(attrs={ 'style': 'height: 30px; font-size: 16px;width:250px ' 
                                  })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove help text for password1 and password2
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['username'].help_text = ''

        self.fields['password1'].widget.attrs = {'style': 'height: 30px; font-size: 16px; width: 250px;'}
        self.fields['password2'].widget.attrs = {'style': 'height: 30px; font-size: 16px; width: 250px;'}
        self.fields['email'].widget.attrs = {'style': 'height: 30px; font-size: 16px; width: 250px;'}
        self.fields['username'].widget.attrs = {'style': 'height: 30px; font-size: 16px; width: 250px;'}
    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2', 
        ]



class UsernameForm(forms.Form):
    username = forms.CharField(
    max_length=30,
    widget=forms.TextInput(attrs={ 'style': 'height: 30px; font-size: 16px;width:250px ' 
                                  }),
    )

class PasswordForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        del self.fields['username']
        self.fields['password'].widget.attrs = {'style': 'height: 30px; font-size: 16px; width: 250px;'}



