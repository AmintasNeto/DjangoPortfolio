# Generated by Django 5.0 on 2023-12-12 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_tag_products_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
