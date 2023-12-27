from django import forms
from django.core.exceptions import ValidationError

from book import models


class AddPostForm(forms.ModelForm):
    class Meta:
        model = models.Books
        fields = ('__all__')

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 150:
            raise ValidationError('LIMIT 200')

        return title
