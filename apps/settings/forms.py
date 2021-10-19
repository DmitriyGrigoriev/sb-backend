from django import forms
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _
from .models import Service

class ServiceModelAdminForm(ModelForm):
    code = forms.CharField(required=True,
                           label=_('Код Услуги'),
                           max_length=20,
                           empty_value=''
                           )
    class Meta:
        model = Service
        fields = '__all__'


class ServicePriceModelAdminForm(BaseInlineFormSet):
    price = forms.DecimalField(required=True)

    def clean(self):
        """Check that at least one service has been entered."""
        super().clean()
        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get('DELETE', False)
            for cleaned_data in self.cleaned_data):
            raise forms.ValidationError(_('Необходимо добавить хотя бы одну цену для «Услуги»'))