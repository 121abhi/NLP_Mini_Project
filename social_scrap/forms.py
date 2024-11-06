from django import forms

class LinkedInForm(forms.Form):
    linkedin_url = forms.URLField(label='LinkedIn Profile URL', max_length = 200, widget= forms.URLInput(attrs= {'placeholder': 'Enter LinkedIn profile URL'}))
    