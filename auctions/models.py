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
    def watching(self):
        return self.watching.all()



"""--------------"""
class Category(models.Model):
    name = models.CharField(max_length=32, null=True)

    def __str__(self):
        return self.name


#     # listing_id= models.ForeignKey('Listing')

"""--------------"""

class Listing(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64)
    start_price = models.FloatField()
    # desired increments ?? (able like choose if 0.1$, or 1$ or 5$ increments)
    image = models.URLField(null=True, blank=True, default="https://static.vecteezy.com/system/resources/thumbnails/006/899/230/small/mystery-random-loot-box-from-game-icon-vector.jpg")
    description = models.TextField(max_length=500, null=True) #remove NULL?
    date = models.DateTimeField(auto_now=True) # editable=False
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE) #MUst be se on [deleted user, but this is  FK and only expects an id Number]
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    # final_buyer ?

    def __str__(self):
        return f"{self.id} - {self.title}. price: {self.start_price}"

    @property
    def is_active(self):
        return self.active

    """# this is a method of an existing listing where i already have a
    l1 = Listing.objects.get(id=1) OBJECT selected in a var
    so that now i can call l1.close_auction() and its own method sets it to False"""

    @property
    def close_auction(self):
        self.active= False
        return("closed")

    def highest_bidder(self):
        bidders = self.bidding.order_by('-bid')
        try:
            bidders.first().bid()
        except:
            return None


"""--------------"""
# Bidding table but also History price
class Bids(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bidding")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid = models.FloatField()
    # max, min validators
    # https://stackoverflow.com/questions/61856270/how-do-i-put-max-and-min-limit-on-django-admin-tables-float-fields
    def __str__(self):
        return f"{self.user}: {self.bid}"

"""--------------"""

class Watchlist(models.Model):
    listing_id = models.ForeignKey(Listing, related_name="watchers", null=True, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(User, related_name="watching", null=True, on_delete=models.SET_NULL)

"""--------------"""
class Comments(models.Model):
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    text = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user_id}: {self.text}"

"""--------------"""

# class User(AbstractUser): #circular dependencies
#     watchlist = models.ManyToManyField(Listing, blank=True, related_name="watcher")
#     pass