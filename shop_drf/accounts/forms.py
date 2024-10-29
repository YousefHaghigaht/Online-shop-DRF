from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password' ,widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password' ,widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number','email','full_name','password','password2')

    def clean_password2(self):
        p1 = self.cleaned_data['password']
        p2 = self.cleaned_data['password2']
        if p1 and p2 and p1 != p2:
            raise ValidationError('Passwords dont match')
        return p2

    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone_number','email','full_name','password','is_admin','is_active','last_login')