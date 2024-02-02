from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record, Group_Record, Sender

# Add Record Form

class AddRecordForm(forms.ModelForm):
    contact_id = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Contact ID",  "class": "form-control"}), label="")
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "First Name",  "class": "form-control"}), label="")
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Last Name",  "class": "form-control"}), label="")
    phone = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Phone Number",  "class": "form-control"}), label="")
    email = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Email Address",  "class": "form-control"}), label="")
    
    class Meta:
        model = Record
        exclude = ("User", )
        
class AddGroupForm(forms.ModelForm):
    
    group_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Group Name",  "class": "form-control"}), label="")
    user = forms.ModelMultipleChoiceField(required=True, queryset=Record.objects, widget=forms.CheckboxSelectMultiple())
    
    class Meta:
        model = Group_Record
        exclude = ("User", )
        
class AddSenderForm(forms.ModelForm):
    phone_number_id = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Phone_ID",  "class": "form-control"}), label="")
    access_token = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Token",  "class": "form-control"}), label="")
    message = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Note",  "class": "form-control"}), label="")
    class Meta:
        model = Sender
        exclude = ("User", )
    
    