from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.logout_view),
    path('homepage/', views.home_page, name='home_page'),
    path("profile/", views.profile, name='profile'),
    path("messaging/", views.messaging, name='messaging'),
    path("lent_items/", views.lent_items, name='lent_items'),
    path("borrowed_items/", views.borrowed_items, name='borrowed_items'),
    path("marketplace/", views.marketplace, name='marketplace'),
    path("librarian_homepage/", views.librarian_home_page, name='librarian_homepage'),
]
