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

    # submit form
    if request.method == "POST":

        # crea dictionary submission
        submission = CreateListing(request.POST)

        # if valid, add owner to the model, then save
        if submission.is_valid():
            submission.instance.owner = request.user
            submission.save()

            listing_id = submission.instance.id # can only get 'id' AFTER save(), else: None
            return HttpResponseRedirect(reverse("item", args=[listing_id]))

        else:
            # maybe redirect with another error
            print("no")


    else: # "GET"

        # NOTES: funziona, sistemare design e cercare di mettere m2m to Category
        create_form = CreateListing()
        context = {'form': create_form}
        return render(request, "auctions/create.html", context)


def item_page(request, id):

    if request.method == "POST":
        # TODO logic for delete from owner
        # TODO logic to bid on item from not owner

        pass

    else: #"GET"
    # render page
        try:
            # ottieni l'id della pagina richiesta per caricare i dati
            item = Listing.objects.get(id=id)

            try:
                usr_watchlist = get_user_watchlist(request.user.id)
                watchlist_ids = get_user_watchlist(request.user.id, only_id=True)
                print(watchlist_ids)

            except:
                print("error in user_watchlist() function")


            try:
                n_ppl_watching = people_watching(item_id=item.id)
            except:
                print("error in people_watching()")

            # try:
            #     user = User.objects.get(request.user.id)
            #     print(user.is_watching(self=user, listing_id=item.id))
            # except:
            #     print("doesn't work like that")


            context = {'item':item, 'people_watching': n_ppl_watching, 'usr_watchlist': watchlist_ids}

            #--------------------
            return render(request, "auctions/item.html", context=context)

        except: # if no page
            return render(request, "auctions/item.html", {'error':"error"})


def watchlist(request, id=None):
    user_watched = user_watched


    if request.method =="POST": # when added to watchlist

        # list_id =
        # user = request.user
        pass

    else: #display the user watched items


        context = {"watchlist":user_watched}


        return render(request, "auctions/watchpage.html", context=context)


# # NOTES FROM create()
# after >>   if request.method == "POST":

        #        submission = CreateListing(request.POST)
        #        if submission.is_valid():
        #            """ 2 different ways of accessing data"""
        #           print(submission.data["title"])
        #           print(submission.instance.title)


# ======== functions ===============

# counts number of occurrences of this listing_id in watchlist table
def people_watching(item_id):
        watchers = Watchlist.objects.filter(listing_id=item_id).count()
        return watchers

# gets objects in user's watchlist
# if as_list=True, only returns list of IDs
def get_user_watchlist(us_id, only_id=False):
        user_watched = Listing.objects.filter(watchers__user_id = us_id)
        if only_id:
            watchlist_ids = [q.id for q in user_watched]
            return watchlist_ids
        return user_watched

# OLD
# def user_watchlist(user_id):
#         user = User.objects.get(id=user_id)
#         queryset = user.watching.all()
#         in_watchlist = [q.id for q in queryset]
#         return in_watchlist
