# Generated by Django 4.1.1 on 2022-10-08 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0023_rename_listing_id_bids_listing_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='listing_id',
        ),
        migrations.AddField(
            model_name='comments',
            name='listing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='commentz', to='auctions.listing'),
            preserve_default=False,
        ),
    ]
