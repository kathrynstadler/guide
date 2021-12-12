from django import forms
from django.forms.widgets import HiddenInput, NumberInput
from .models import Reviews
from .models import Request

class ReviewsPost(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ["location", "review"]
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'review': forms.Textarea(attrs={'class': 'form-control'}),
        }

class RequestPost(forms.ModelForm):
    class Meta:
        model = Request
        fields = ["name", "address"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SMSForm(forms.Form):
    #phone_number = forms.CharField(label='Your Number', min_length=10, max_length=10)
    dir_message = forms.TextInput()
    '''
    # clean the number for 
    def clean_phone(self):
        data = self.cleaned_data['phone_number']
    '''