# Generated by Django 5.0 on 2023-12-13 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_products_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='notes',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
