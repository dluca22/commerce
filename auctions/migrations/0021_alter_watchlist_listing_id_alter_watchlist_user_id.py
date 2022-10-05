# Generated by Django 4.1.1 on 2022-10-05 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_alter_watchlist_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='listing_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='watchers', to='auctions.listing'),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='watching', to=settings.AUTH_USER_MODEL),
        ),
    ]