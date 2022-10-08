from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm, modelformset_factory
from .models import *
from django import forms

# =============form model=============
class CreateListing(ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'
        exclude = ('owner',)

# ============= bid form =============

class PlaceBid(ModelForm):
    class Meta:
        model = Bids
        fields = ('bid',)

# ============= index page =============
def index(request):
    items_database = Listing.objects.all()
    context = {'items_database' : items_database}
    return render(request, "auctions/index.html", context=context)

# ============= login page =============
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

# ============= logout page =============
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# ============= register page =============
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


# ============= create listing =============
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
        context = {'create_form': create_form}
        return render(request, "auctions/create.html", context)

# ============= item page =============

def item_page(request, id):

    if request.method == "POST":
        # TODO logic for delete from owner
        # TODO logic to bid on item from not owner

        pass

    else: #"GET"
    # render page

        u=request.user.id

        # non funziona piu item page per user not authenticated

        print(request.user == "AnonymousUser")

        try:
            # ottieni l'id della pagina richiesta per caricare i dati
            item = Listing.objects.get(id=id)
            bid_form= PlaceBid()
            try:
                n_ppl_watching = people_watching(item.id)
            except:
                print("error in people_watching()")

            try:
                usr = request.user
                is_watching = usr.is_watching(item.id)
            except:
                print("error in usr.is_watching()")

            context = {'item':item, 'people_watching': n_ppl_watching, 'is_watching': is_watching, 'bid_form': bid_form}

            return render(request, "auctions/item.html", context=context)

        except: # if no page
            return render(request, "auctions/item.html", {'error':"error"})

# ============= watchlist page =============

def watchlist(request):
    #display the user watched items
    # can be shortened without try/except
    try:
        # sometimes only works with request.user.id
        user_watchlist = get_user_watchlist(request.user)
    except:
        print("error in user_watchlist() function")

    return render(request, "auctions/watchpage.html",{"watchlist":user_watchlist})

# ============= watch toggle function =============

# watch toggle sends listing id and get value from button
# WHY DEFAULT NONE???
def watch_toggle(request, li_id=None): # DONE
    if request.method =="POST":
        print("QUAA QUAA QUAA")
        print(li_id)
        print("QUAA QUAA QUAA")
        user = request.user
        # if follow, creates entry in database
        if request.POST['watch_toggle'] == "follow":

            listing = Listing.objects.get(id=li_id)

            if not user.is_watching(listing):
                watch = Watchlist(user_id=user, listing_id=listing)
                watch.save()

        # unfollow, removes entry from db
        elif request.POST['watch_toggle'] == "unfollow":
            if user.is_watching(listing_id=li_id):
                watch = Watchlist.objects.get(user_id=request.user.id, listing_id=li_id)
                watch.delete()

        # return item page (seem like a non refresh item page)
        return HttpResponseRedirect(reverse("item", args=[li_id]))

# ============= bid function =============

def bid(request, li_id):
    if request.method == "POST":
        # submission = CreateListing(request.POST)
            # submission.is_valid()
        form = PlaceBid(request.POST)
        # form is a valid float
        if form.is_valid():
            bid = form.instance.bid
            listing = Listing.objects.get(id=li_id)


            # error check if bid > 0 (or via model class)

            # highest = listing.highest_bidder().bid
            highest = listing.highest_bidder()
            print(f"highest as num {highest}")
            # if there is no bid registered for the auction se to start_price
            if highest == None:
                highest = Listing.start_price

            if bid <= highest:
                error = "Your bid must be higher"
            if bid > highest:
                place_bid = Bids(listing=listing, user=request.user, bid=bid)
                place_bid.save()
        # ele: bid not valid -> error message
    return HttpResponseRedirect(reverse("item", args=[li_id]))



# ============= close auction =============
def close_auct(request, li_id):
    if request.method == "POST":
        winner = li_id.highest_bidder()
        print("non è chiusa questa FUNC")
        print(winner)
        pass


# =================================
# ============= NOTES =============
# =================================

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


def get_user_watchlist(us_id):
        user_watched = Listing.objects.filter(watchers__user_id = us_id)

        return user_watched #return QuerySet

# =====================================================
# DISCARDED because they return Querysets of Watchlist objects
# def DISCARDEDget_user_watchlist(user):
#         user_watched = user.watching.filter(user_id = user)
#         return user_watched #return QuerySet

# # #same
# def DISCARDED2get_user_watchlist(us):
#     user_watched = Watchlist.objects.filter(user_id = us)
#     return user_watched.values() #return QuerySet
# =====================================================


# OLD
# def user_watchlist(user_id):
#         user = User.objects.get(id=user_id)
#         queryset = user.watching.all()
#         in_watchlist = [q.id for q in queryset]
#         return in_watchlist


# notes from watch_toggle
""" mettere server-side checking in caso di trickery su HTML
            >>> l1.watchers
                <django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager.<locals>.RelatedManager object at 0x7fd720e77100>
            >>> l1.watchers.all()
                <QuerySet [<Watchlist: Watchlist object (1)>]>
            >>> l1.watchers.get()
                <Watchlist: Watchlist object (1)>
            >>> wa = l1.watchers.get()
            >>> wa.user_id
                <User: luca>
    """