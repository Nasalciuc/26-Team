from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class ScrapingForm(forms.Form):
    url = forms.URLField(
        label='URL Site',
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com',
            'required': True
        }),
        help_text='Introduceți URL-ul complet al site-ului pe care doriți să îl analizați'
    )
    
    def clean_url(self):
        url = self.cleaned_data['url']
        # Validare suplimentară
        if not url.startswith(('http://', 'https://')):
            raise ValidationError('URL-ul trebuie să înceapă cu http:// sau https://')
        return url 