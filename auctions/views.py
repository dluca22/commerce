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
            print("submission CreateListing() NOT VALID")


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

            user = User.objects.get(id=request.user.id)

            try:
                n_ppl_watching = people_watching(item.id)

            except:
                print("error in people_watching()")

            try:
                is_watching = user.is_watching(item.id)
                print(f" ln 134 {is_watching}")

            except:
                print("errore qui 137")

            context = {'item':item, 'people_watching': n_ppl_watching, 'is_watching': is_watching}

            return render(request, "auctions/item.html", context=context)

        except: # if no page
            return render(request, "auctions/item.html", {'error':"error"})


def watchlist(request):
    #display the user watched items
    # can be shortened without try/except
    try:
        user_watchlist = get_user_watchlist(request.user.id)
    except:
        print("error in user_watchlist() function")

    return render(request, "auctions/watchpage.html",{"watchlist":user_watchlist})



def watch_toggle(request, id=None):
    if request.method =="POST": # when added to watchlist
        # item = Listing.object.get(id=1)
        if request.POST['watch_toggle'] == "follow":
            user = User.objects.get(id=request.user.id)
            listing = Listing.objects.get(id=id)
            watch = Watchlist.objects.create(user_id=user, listing_id=listing)
            watch.save()

        elif request.POST['watch_toggle'] == "unfollow":
            watch = Watchlist.objects.get(user_id=request.user.id, listing_id=id)
            watch.remove()


        return HttpResponseRedirect(reverse("item", args=[id]))


# # NOTES FROM create()
# after >>   if request.method == "POST":

        #        submission = CreateListing(request.POST)
        #        if submission.is_valid():
        #            """ 2 different ways of accessing data"""
        #           print(submission.data["title"])
        #           print(submission.instance.title)


# ======== functions ===============

# counts number of occurrences of this listing_id in watchlist table
def people_watching(item_id) -> int:
        watchers = Watchlist.objects.filter(listing_id=item_id).count()
        return watchers

# gets objects in user's watchlist
def get_user_watchlist(us_id):
        user_watched = Listing.objects.filter(watchers__user_id = us_id)
        print(type(user_watched))
        return user_watched #return QuerySet

# OLD
# def user_watchlist(user_id):
#         user = User.objects.get(id=user_id)
#         queryset = user.watching.all()
#         in_watchlist = [q.id for q in queryset]
#         return in_watchlist
