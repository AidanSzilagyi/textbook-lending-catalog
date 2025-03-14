from django.urls import path
from . import views

urlpatterns = [
    path("login", views.index, name="index"),
    path("logout", views.logout_view),
    path("", views.home_page, name='home_page'),
    path("profile/", views.profile, name='profile'),
    path("messaging/", views.messaging, name='messaging'),
    path("lent_items/", views.lent_items, name='lent_items'),
    path("borrowed_items/", views.borrowed_items, name='borrowed_items'),
    path("marketplace/", views.marketplace, name='marketplace'),
    path("librarian_home_page/", views.librarian_home_page, name='librarian_home_page'),
    path("homepage/", views.home_page_router, name='home_page_router'),
    path("librarian_settings/", views.librarian_settings, name='librarian_settings'),
    path("patron_to_librarian/", views.patron_to_librarian, name='patron_to_librarian'),
]
