from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm, modelformset_factory
from .models import *
from django.contrib import messages


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
# ============= comment form =============

class AddComment(ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)

# ============= index page =============
def blank(request):
    return render(request, 'auctions/blank.html')
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
            return render(request, "auctions/create.html", {'create_form': submission})


    else: # "GET"

        # NOTES: funziona, sistemare design e cercare di mettere m2m to Category
        create_form = CreateListing()

        return render(request, "auctions/create.html", {'create_form': create_form})

# ============= item page =============

def item_page(request, id, bid_error=None):
    try:
        # ottieni l'id della pagina richiesta per caricare i dati
        item = Listing.objects.get(id=id)
        bid_form= PlaceBid()
        comment_form = AddComment()

        try:
            usr = request.user
            is_watching = usr.is_watching(item.id)
        except:
            print("error in usr.is_watching()")

        context = {'item':item, 'is_watching': is_watching, 'bid_form': bid_form,'comment_form': comment_form, 'bid_error': bid_error}

        return render(request, "auctions/item.html", context=context)

    except: # if no page
        error = "this fucking thing"

        return render(request, "auctions/item.html", {'error':error})

# ============= all categories page =============
def categories(request):
    all_categories = Category.objects.all()

    return render(request, "auctions/all_categories.html", {'display_all': True, 'all_categories':all_categories})

# ============= selected categories page =============
def in_category(request, categ_name):

    try:
        category = Category.objects.get(name = categ_name)
        items_in_cat = category.active_in_category
    except:
        wrong = categ_name.capitalize()
        return render(request, "auctions/all_categories.html", {'error': wrong})

    return render(request, "auctions/all_categories.html", {'category':category, 'show_in_this_category': True, 'items_in_cat': items_in_cat})


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

            curret_price = listing.current_bid()

            if bid <= curret_price:
                # error = messages.add_message(request, messages.INFO, "Your bid can't be lower than the current price")
                # return item_page(request, li_id, error=error)
                messages.add_message(request, messages.ERROR, "Your Bid can't be lower than the current price!")

            if bid > curret_price:
                place_bid = Bids(listing=listing, user=request.user, bid=bid)
                place_bid.save()

    return HttpResponseRedirect(reverse("item", args=[li_id]))


# ============= close auction =============
# calls close_auct property, then saves
def close_auct(request, li_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=li_id)
        listing.close_auction
        listing.save()
        return HttpResponseRedirect(reverse("item", args=[li_id]))

# ============= add comment =============
# gets comment body from post form, saves entry to db, redirects to item page
def add_comment(request, li_id):
    if request.method == "POST":
        commentform = AddComment(request.POST)
        if commentform.is_valid():
            body = commentform.instance.text
            listing = Listing.objects.get(id=li_id)
            add_comment = Comments(listing=listing, user=request.user, text=body)
            add_comment.save()
        return HttpResponseRedirect(reverse("item", args=[li_id]))


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