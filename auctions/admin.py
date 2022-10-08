from django.contrib import admin

from .models import *

# class ListingAdmn(Listing):
#     readonly_fields = ('date',)


# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Watchlist)
admin.site.register(Comments)
admin.site.register(Bids)
