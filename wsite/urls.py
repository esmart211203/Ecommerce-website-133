from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .templatetags import cart_tags
urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about_page, name="about"),
    path("contact", views.contact_page, name="contact"),
    path("shop", views.shop_view, name="shop.index"),
    path("shop-category/<int:category_id>", views.shop_category, name="shop.category"),
    path("search", views.search, name="search"),
    path("profile", views.profile, name="profile"),
    path("change-password", views.change_password, name="change-password"),
    #### CART & ORDER ####
    path("order", views.order_view, name="order.index"),
    path("order-detail/<int:order_id>", views.order_detail, name="order.detail"),
    path("order-completed/<int:order_id>", views.order_completed, name="order.completed"),
    path("delete-order/<int:order_id>", views.delete_order, name="order.delete"),
    path("cart", views.cart_view, name="cart"),
    path("add-to-cart/<int:product_id>", views.add_to_cart, name="cart.store"),
    path("delete-cart-item/<int:item_id>", views.delete_cart_item, name="cart.delete"),
    path("increase-quantity/<int:item_id>", views.increase_quantity, name="increase.quantity"),
    path("decrease-quantity/<int:item_id>", views.decrease_quantity, name="decrease.quantity"),
    path("check-out", views.checkout, name="checkout"),
    path("checkout-info", views.checkout_info, name="checkout-info"),
    #### ADMIN ####
    path("view-admin", views.admin_view, name="admin"),
    ### CATEGORY ###
    path("category", views.category_view, name="category.index"),
    path("create-category", views.CreateCategoryView.as_view(), name="category.create"),
    path("delete-category/<int:category_id>", views.delete_category, name="category.delete"),
    path("edit-category/<int:category_id>", views.EditCategoryView.as_view(), name="category.edit"),
    ### PRODUCT ###
    path("product", views.product_view, name="product.index"),
    path("detail-product/<int:product_id>", views.detail_product, name="product.detail"),
    path("create-product", views.CreateProductView.as_view(), name="product.create"),
    path("delete-product/<int:product_id>", views.delete_product, name="product.delete"),
    path("edit-product/<int:product_id>", views.EditProductView.as_view(), name="product.edit"),
    ### USER ###
    path("user", views.user_view, name="user.index"),
    path("delete-user/<int:user_id>", views.delete_user, name="user.delete"),
    ### AUTH ###
    path("login", views.LoginView.as_view(), name="login"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("logout", views.logout_user, name="logout"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)