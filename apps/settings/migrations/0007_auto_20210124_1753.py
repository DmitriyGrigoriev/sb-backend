# Generated by Django 3.1 on 2021-01-24 17:53

from decimal import Decimal
from django.db import migrations, models
import djmoney.models.fields
import djmoney.models.validators


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0006_auto_20210124_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceprice',
            name='unit_price_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'Euro'), ('RUB', 'Russian Ruble'), ('USD', 'US Dollar')], default='RUB', editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='serviceprice',
            name='unit_price',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='RUB', max_digits=18, validators=[djmoney.models.validators.MinMoneyValidator(Decimal('0.01000000000000000020816681711721685132943093776702880859375'))], verbose_name='Цена Единицы'),
        ),
        migrations.AlterField(
            model_name='vatpostinggroup',
            name='vat',
            field=models.DecimalField(decimal_places=2, max_digits=18, verbose_name='НДС %'),
        ),
    ]
