# Generated by Django 4.1.1 on 2022-10-04 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_listing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(default='None', max_length=32, null=True),
        ),
    ]
