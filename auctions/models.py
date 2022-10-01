from dataclasses import Field
from unicodedata import category
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # pass

class User(models.Model):
    id = models.AutoField()
    username = models.CharField(max_length=32)
    email = models.EmailField()
    password = models.password
    userimage (if any)


class Listing(models.Model):

    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64)
    price = models.FloatField()
    image = models.URLField()
    description = models.TextField(max_length=500)
    date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    category = models.ForeignKey('Category')
    active = models.BooleanField()

    def __str__(self):
        return f"{self.id}: {self.title}. Price: {self.price}"



# Listing():
    #     id
    #     title
    #     price
    #     image
    #     description
    #     date
    #     owner F.K.
    #     category F.K.
    #     active (bool)
"""--------------"""

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=32)
    # listing_id= models.ForeignKey('Listing')

"""--------------"""

# Watchlist()
#     listing_id
#     user_id
"""--------------"""
# Comments()
#     listing_id
#     user_id
#     text
"""--------------"""
# forse
    # History_price()
"""--------------"""
