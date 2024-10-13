
from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from store.models import UserProfile,Product,Ordersummary,Reviews


class SignUpForm(UserCreationForm):

    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":" mt-2 flex h-10 w-full rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-gray-400 focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50","placeholder":"Password"}))

    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":" mt-2 flex h-10 w-full rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-gray-400 focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50","placeholder":"Conform Password"}))

    class Meta:

        model=User

        fields=["username","email","password1","password2"]

        widgets={
            "username":forms.TextInput(attrs={"class":" mt-2 flex h-10 w-full rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-gray-400 focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50","placeholder":"Full Name"}),

            "email":forms.EmailInput(attrs={"class":"mt-2 flex h-10 w-full rounded-md border border-gray-300 bg-transparent px-3 py-2 text-sm placeholder:text-gray-400 focus:outline-none focus:ring-1 focus:ring-gray-400 focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50","placeholder":"Email"})
        }

class SignInForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control mb-2"}))

    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mb-2"}))


class UserProfileForm(forms.ModelForm):

    class Meta:

        model=UserProfile

        fields=["bio","profile_pic"]

        widgets={
            "bio":forms.TextInput(attrs={"class":"w-full border p-2 my-3"}),
            "profile_pic":forms.FileInput(attrs={"class":"w-full border p-2 my-3"})
        }


class DelivaryaddressForm(forms.ModelForm):

    class Meta:

        model=Ordersummary

        fields=["name","address","pincode","phone","payment_method"]

        widgets={
            
            "name":forms.TextInput(attrs={"class":"w-full border p-2 my-3"}),
            "address":forms.TextInput(attrs={"class":"w-full border p-2 my-5",'rows':3}),
            "pincode":forms.TextInput(attrs={"class":"w-full border p-2 my-3"}),
            "phone":forms.TextInput(attrs={"class":"w-full border p-2 my-3"}),
            "payment_method":forms.Select(attrs={"class":"w-full border p-2 my-3 form-select"}),
        }


class ReviewForm(forms.ModelForm):

    class Meta:

        model=Reviews

        fields=["comment","rating"]

        widgets={
            "comment":forms.Textarea(attrs={"class":"w-full border p-2 my-3","rows":5}),
            # "rating":forms.Select(attrs={"class":"w-full border p-2 my-3"})
        }





