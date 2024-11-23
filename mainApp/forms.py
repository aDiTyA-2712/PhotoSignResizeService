from django import forms

class ImageUpForm(forms.Form):
    profile_pic=forms.ImageField(label="Upload your Image")
    sign_pic=forms.ImageField(label="Upload your signature")

    profile_width = forms.IntegerField(label="Image Width")
    profile_height = forms.IntegerField(label="Image Height")

    sign_width = forms.IntegerField(label="Signature Width")
    sign_height = forms.IntegerField(label="Signature Height")
