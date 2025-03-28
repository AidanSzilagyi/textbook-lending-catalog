from django.urls import path
from . import views

urlpatterns = [
    path("login", views.index, name="index"),
    path("logout", views.logout_view),
    path("", views.home_page, name='home_page'),
    path("profile/", views.profile, name='profile'),
    path('classes/create/', views.class_create, name='class_create'),
    path('classes/<slug:slug>/material_create/', views.material_create, name='material_create'),
    path("messaging/", views.messaging, name='messaging'),
    path("lent_items/", views.lent_items, name='lent_items'),
    path("borrowed_items/", views.borrowed_items, name='borrowed_items'),
    path("marketplace/", views.marketplace, name='marketplace'),
    path("librarian_home_page/", views.librarian_home_page, name='librarian_home_page'),
    path("homepage/", views.home_page_router, name='home_page_router'),
    path("required_materials/", views.required_materials, name='required_materials'),
    path('classes/<slug:slug>/', views.class_detail, name='class_detail'),
    path("upload_pfp/", views.upload_pfp, name="upload_pfp"),
    path("librarian_settings/", views.librarian_settings, name='librarian_settings'),
    path("patron_to_librarian/", views.patron_to_librarian, name='patron_to_librarian'),
    path('add-item/', views.add_item, name='add_item'),
    path('add-item-submit/', views.add_item_submit, name='add_item_submit'),
    path('tag_create/', views.tag_create, name='tag_create'),
    path('classes/<slug:slug>/unlink_material/<int:item_id>/', views.unlink_material, name='unlink_material'),
]
