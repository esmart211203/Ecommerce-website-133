from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    #### ADMIN ####
    path("view-admin", views.admin_view, name="admin:index"),
    path("product", views.product_view, name="product"),
    path("category", views.category_view, name="category"),
    path("user", views.user_view, name="user"),
    ### AUTH ###
    path("login", views.LoginView.as_view(), name="login"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("logout", views.logout_user, name="logout"),
]