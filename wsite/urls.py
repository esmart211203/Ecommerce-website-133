from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    #### ADMIN ####
    path("view-admin", views.admin_view, name="admin_index"),
    path("product", views.product_view, name="product"),
    path("category", views.category_view, name="category"),
    path("user", views.user_view, name="user"),
]