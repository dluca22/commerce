from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categories", views.categories, name="categories"),
    path("cat=<str:categ_name>", views.in_category, name="category"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("item/<int:id>", views.item_page, name="item"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watch <int:li_id>", views.watch_toggle, name="watch_toggle"),
    path("close <int:li_id>", views.close_auct, name="close"),
    path("bid <int:li_id>", views.bid, name="bid"),
    path("add_comment <int:li_id>", views.add_comment, name="comment")
]
