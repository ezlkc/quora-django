from django import forms
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta:
        fields = ['username', 'password']


class ProfileForm(forms.ModelForm):
    education = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), required=False)
    profession = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), required=False)
    employment = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}), required=False)
    avatar = forms.FileField(widget=forms.FileInput(), required=False)

    def __init__(self, *args, **kwargs):
        if kwargs:
            profession = kwargs.pop("profession")  # kullanıcıdan, views.py'den aktarılan parametredir
            employment = kwargs.pop("employment")
            education = kwargs.pop("education")
            super(ProfileForm, self).__init__(*args, **kwargs)
            self.fields['profession'] = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'value': profession}), required=False)
            self.fields['employment'] = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'value': employment}), required=False)
            self.fields['education'] = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'value': education}), required=False)
        else:
            super(ProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Profile
        fields = ['education', 'profession', 'employment', 'avatar']
