from django import forms
from django.forms import ModelForm, ValidationError

from .models import Service

class ServiceModelAdminForm(ModelForm):
    class Meta:
        model = Service
        fields = '__all__'

    # def clean_blocked(self):
    #     result = True
    #     cleaned_data = super().clean()
    #     blocked = cleaned_data.get('blocked')
    #     if blocked:
    #         result = False
    #         raise forms.ValidationError('invalid!')
    #     return result
