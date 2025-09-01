from django import forms
from .models import Event, Participant, Category
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission, Group
from tasks.forms import Styledformixin
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ["username", "password1", "password2"]:
            self.fields[fieldname].help_text = None

class CustomRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password"), cleaned.get("confirm_password")
        if not p1 or len(p1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        if p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = False 
        if commit:
            user.save()
        return user



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']


class AssignRoleForm(Styledformixin, forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role"
    )
    
class CreateGroupForm(Styledformixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permission'
    )
    
    class Meta:
        model = Group
        fields = ['name', 'permissions']
