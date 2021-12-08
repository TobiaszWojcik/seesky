from django.forms import ModelForm
from .models import Newsletter


class NewsletterForm(ModelForm):
    class Meta:
        model = Newsletter
        fields = [
            'name',
            'place',
            'lat',
            'lon',
            'email',
            'token',
            'email_time'
        ]
