from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import User
from account.models import Sector


class SignupForm(UserCreationForm):
    
    email = forms.EmailField(max_length=255, required=True, 
                                widget=forms.widgets.Input(
            attrs={"placeholder": "Enter email address.","class": "w-full input input-bordered input-md bg-white block py-1 sm:text-sm sm:leading-2 label text-sm text-gray600", }),
            label="Email address",)
    phone_number = forms.CharField(max_length=50, required=True, 
                                widget=forms.widgets.Input(
            attrs={"placeholder": "Enter phone number.","class": "w-full input input-bordered input-md bg-white block py-1 sm:text-sm sm:leading-2 label text-sm text-gray600", }),
            label="Phone number",)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter password","class": "w-full input input-bordered input-md bg-white block py-1 sm:text-sm sm:leading-2 label text-sm text-gray600", }),
                                label="Enter password",)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm password","class": "w-full input input-bordered input-md bg-white block py-1 sm:text-sm sm:leading-2 label text-sm text-gray600", }),
                                label="Confirm password",)


    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password1', 'password2']


class LoginForm(forms.Form):
    email = forms.CharField(max_length=63, widget=forms.widgets.Input(
            attrs={"placeholder": "Enter email.","class": "w-full input input-bordered input-md bg-white block py-1 sm:text-sm sm:leading-4", }),)
    password = forms.CharField(max_length=63,  widget=forms.PasswordInput(
        attrs={"placeholder": "**********","class": "mt-2 w-full input input-bordered input-md bg-white block py-1 sm:text-sm sm:leading-4", }),)



class ProfileForm(forms.ModelForm):
    company_name = forms.CharField(max_length=50, required=True,
        widget=forms.widgets.Input(
            attrs={"placeholder": "Enter company name.","class": "w-full input input-bordered input-md bg-white block py-1 sm:text-sm sm:leading-2 label text-sm text-gray600", }),
            label="Company name",)
    address = forms.CharField(max_length=50, required=True,
        widget=forms.widgets.Input(
            attrs={"placeholder": "Enter company address.","class": "w-full input input-bordered input-md bg-white block py-1 sm:text-sm sm:leading-2 label text-sm text-gray600", }),
            label="Company address",)
    rc_number = forms.CharField(max_length=50, required=True,
                                widget=forms.widgets.Input(
            attrs={"placeholder": "Enter RC Number.","class": "w-full input input-bordered input-md bg-white block py-1 sm:text-sm sm:leading-2 label text-sm text-gray600", }),
            label="RC Number",)
    email = forms.EmailField(max_length=255, required=True, 
                                widget=forms.widgets.Input(
            attrs={"placeholder": "Enter email address.","class": "w-full input input-bordered input-md bg-white block py-1 sm:text-sm sm:leading-2 label text-sm text-gray600", }),
            label="Email address", disabled=True)
    phone_number = forms.CharField(max_length=50, required=True, 
                                widget=forms.widgets.Input(
            attrs={"placeholder": "Enter phone number.","class": "w-full input input-bordered input-md bg-white block py-1 sm:text-sm sm:leading-2 label text-sm text-gray600", }),
            label="Phone number",)
    
    class Meta:
        model = User
        fields = ['company_name', 'address', 'rc_number', 'phone_number', 'email']
        
        
# class circleform(forms.ModelForm):
#     class Meta:
#     model = curd
#     fields = ['Zone','Circle','circle_code','circle_address'] 
    
#     widgets = {
#         'Zone':forms.Select(attrs = {'class':'form-control'}),
#         'Circle':forms.TextInput(attrs = {'class':'form-control'}),
#         'circle_code':forms.TextInput(attrs = {'class':'form-control'}),
#         'circle_address':forms.TextInput(attrs = {'class':'form-control'}),
#     }  