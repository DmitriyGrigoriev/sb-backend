# Generated by Django 3.1 on 2021-01-24 17:30

from decimal import Decimal
from django.db import migrations
import djmoney.models.fields
import djmoney.models.validators


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0005_auto_20210124_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='unit_price',
            field=djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), default_currency='RUB', max_digits=18, validators=[djmoney.models.validators.MinMoneyValidator(Decimal('0.01000000000000000020816681711721685132943093776702880859375'))], verbose_name='Цена Единицы'),
        ),
    ]