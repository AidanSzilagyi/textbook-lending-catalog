from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("logout", views.logout_view),
    path('home_page/', views.home_page, name='home_page'),
    path("profile/", views.profile, name='profile'),
    path("messaging/", views.messaging, name='messaging'),
    path("lent_items/", views.lent_items, name='lent_items'),
    path("borrowed_items/", views.borrowed_items, name='borrowed_items'),
    path("marketplace/", views.marketplace, name='marketplace'),
    path("librarian_home_page/", views.librarian_home_page, name='librarian_home_page'),
    path("homepage/", views.home_page_router, name='home_page_router'),
    path("upload_pfp/", views.upload_pfp, name="upload_pfp")
]
