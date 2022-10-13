from email.policy import default
from tkinter import CASCADE
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def is_watching(self, listing_id):
        try:
            # errore qui
            self.watching.get(listing_id=listing_id)
            return True
        except:
            return False

    # gives watchers count to item page
    @property
    def watching(self):
        return self.watching.all().count()

# ================================================================
class Category(models.Model):
    name = models.CharField(max_length=32, null=True)

    def __str__(self):
        return self.name

    @property
    def active_in_category(self):
        return self.categorized.filter(active=True)

    def all_categories(self):
        return self.objects.all()

# ================================================================
class Listing(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64)
    start_price = models.FloatField()
    image = models.URLField(null=True, blank=True)
    description = models.TextField(max_length=500, null=True) #remove NULL?
    date = models.DateTimeField(auto_now=True) # editable=False
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="categorized")
    # final_buyer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.title}. price: {self.start_price}"

    # returns active status
    @property
    def is_active(self):
        return self.active

    """# this is a method of an existing listing where i already have a
    l1 = Listing.objects.get(id=1) OBJECT selected in a var
    so that now i can call l1.close_auction() and its own method sets it to False"""

    # toggle to set auction to inactive
    @property
    def close_auction(self):
        self.active= False
    # num people watching for item.html
    @property
    def num_watching(self):
        return self.watchers.count()
    # returns a snippet of the description
    @property
    def descr_snippet(self):
        return f"{self.description[:25]} ..."
    # returns all comments objects for this listing
    @property
    def comments(self):
        return self.commentz.all()

    # return highest bid, if none, return start_price
    def current_bid(self):
        # if there is a bid recorded, else return the start price
        bids = self.bidding.order_by('-bid')
        try:
            return bids.first().bid
        except:
            return self.start_price

    def highest_bidder(self):
        # if there is a bid recorded, else return the start price
        bidders = self.bidding.order_by('-bid')
        try:
            return bidders.first()
        except:
            return self.start_price



# ================================================================
# Bidding table but also History price
class Bids(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidding")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid = models.FloatField()
    # max, min validators
    # https://stackoverflow.com/questions/61856270/how-do-i-put-max-and-min-limit-on-django-admin-tables-float-fields
    def __str__(self):
        return f"{self.user_id}: {self.bid}"

# ================================================================

class Watchlist(models.Model):
    listing_id = models.ForeignKey(Listing, related_name="watchers", null=True, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(User, related_name="watching", null=True, on_delete=models.SET_NULL)

# ================================================================
class Comments(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commentz")
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    text = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user}: {self.text}"
