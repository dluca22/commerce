from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm, modelformset_factory
from .models import *
from django import forms



class CreateListing(ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'
        exclude = ('owner',)

def index(request):
    items_database = Listing.objects.all()
    context = {'items_database' : items_database}
    return render(request, "auctions/index.html", context=context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")





@login_required
def create(request):

    if request.method == "POST":
        # submit form
        # crea dictionary submission
        submission = CreateListing(request.POST)
        if submission.is_valid():
            # if valid, add owner to the model, then save
            submission.instance.owner = request.user
            submission.save()

            # can only get 'id' AFTER save() | <else> None
            listing_id = submission.instance.id
            return HttpResponseRedirect(reverse())
        else:
            print("no")

        return HttpResponseRedirect("")
    else:

        create_form = CreateListing()
        context = {'form': create_form}
        return render(request, "auctions/create.html", context)


def item_page(request, id):

    if request.method == "POST":
        # logic for delete from owner
        pass
    else: #"GET"
    # render page
        try:
            item = Listing.objects.get(id=id)
            total_watching = Watchlist.objects.filter(listing_id=id)
            context = {'item':item, 'total_watching': len(total_watching)}


            return render(request, "auctions/item.html", context=context)
        except:
            return render(request, "auctions/item.html", {'error':"error"})


def watchlist(request, id=None):
    if request.method =="POST":
        # list_id =
        # user = request.user
        pass
    else:
        user_watched = Watchlist.objects.filter(user_id = request.user)


        context = {"watchlist":user_watched}

        return render(request, "auctions/watchpage.html", context=context)




# # NOTES FROM create()
# after >>   if request.method == "POST":

        #        submission = CreateListing(request.POST)
        #        if submission.is_valid():
        #            """ 2 different ways of accessing data"""
        #           print(submission.data["title"])
        #           print(submission.instance.title)
