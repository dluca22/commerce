from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("item/<int:id>", views.item_page, name="item"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watch<int:id>", views.watch_toggle, name="watch_toggle"),
    # path(r"watch/(?P<id>\w+)?", views.watchlist, name="watchlist"),
]
