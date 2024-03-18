import os
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden, HttpResponseNotFound
from .forms import RegistrationForm
from django.contrib.auth.models import User
from .models import Category,Product,CartItem,OrderItem,Order
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
######## FRONT-END #######
def index(request):
    categories = Category.objects.all()[:4]
    context = {
        'categories': categories,
    }
    return render(request, 'index.html', context)

def shop_view(request):
        categories = Category.objects.all()
        products = Product.objects.all()
        context = {
            'products': products,
            'categories': categories,
        }
        return render(request, 'shop.html',context)

def shop_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'media_url': settings.MEDIA_URL,
    }
    return render(request, 'shop_category.html', context)

def detail_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'detail_product.html', {'product': product})

@login_required(login_url="login")
@user_passes_test(lambda u: u.is_superuser, login_url="login")
def is_admin(request):
    if request.user.is_superuser:
        return redirect("admin:index")
    else:
        return HttpResponseForbidden("Access Denied")
    

########## AUTH ##########
class LoginView(View):
    def get(self, request):
        return render(request, "auth/login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            context = {
                "error_message": "Đăng nhập không thành công. Vui lòng kiểm tra lại tên người dùng và mật khẩu."
            }
            return render(request, "auth/login.html", context)
        login(request, user)
        return redirect("index")
class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, "auth/register.html", {"form": form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect("index")
        else:
            return render(request, "auth/register.html", {"form": form})

def logout_user(request):
    logout(request)
    return redirect('index')
########## ADMIN #########

def admin_view(request):
    return render(request, 'admin/index.html')

def order_view(request):
    orders = Order.objects.all()
    return render(request, 'admin/order/index.html',context={'orders': orders})

def order_detail(request,order_id):
    order = get_object_or_404(Order, pk=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'admin/order/detail.html', context={'order_items':order_items})
def product_view(request):
    products = Product.objects.all()    
    return render(request, 'admin/product/index.html', context={'products':products})
class CreateProductView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'admin/product/create.html',context={'categories':categories})
    
    def post(self, request):
        name = request.POST.get("name")
        description = request.POST.get("description")
        image = request.FILES.get("image")
        price = request.POST.get("price")
        category_id = request.POST.get("category")
        featured = request.POST.get("featured") == "on"
        category = get_object_or_404(Category, pk=category_id)
        #create
        product = Product(name=name, description=description, image=image, price=price, category=category, featured=featured)
        product.save()

        return redirect("product.index")

class EditProductView(View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        categories = Category.objects.all()
        return render(request, 'admin/product/edit.html', context={'product': product, 'categories': categories})

    def post(self, request, product_id):
        product = get_object_or_404(Product, pk=product_id)
        name = request.POST.get("name")
        image = request.FILES.get("image")
        description = request.POST.get("description")
        price = request.POST.get("price")
        category_id = request.POST.get("category")
        featured = request.POST.get("featured") == "on"

        # Lấy đối tượng Category từ category_id
        category = get_object_or_404(Category, pk=category_id)

        # Kiểm tra xem người dùng đã chọn ảnh mới hay không
        if image:
            # Nếu có, xóa ảnh cũ
            if product.image:
                os.remove(product.image.path)
            product.image = image
        else:
            # Nếu không, sử dụng ảnh cũ
            image = product.image

        # Cập nhật thông tin của sản phẩm
        product.name = name
        product.description = description
        product.price = price
        product.category = category
        product.featured = featured
        product.save()

        return redirect("product.index")
    

def delete_product(request, product_id):
    try:
        product = get_object_or_404(Product, pk=product_id)
        if product.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(product.image))
            if os.path.exists(image_path):
                os.remove(image_path)
        
        product.delete()
        return redirect("product.index")
    except Http404:
        return HttpResponseRedirect(reverse('product_not_found'))

def category_view(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'admin/category/index.html', context)

class CreateCategoryView(View):
    def get(self, request):
            return render(request, 'admin/category/create.html')
    
    def post(self, request):
        name = request.POST.get("name")
        image = request.FILES.get("image")
        description = request.POST.get("description")
        featured = request.POST.get("featured") == "on"
        category = Category(name=name, image=image, description=description, featured=featured)
        category.save() 
        return redirect("category.index")
class EditCategoryView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        return render(request, 'admin/category/edit.html', context={'category': category})

    def post(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        name = request.POST.get("name")
        image = request.FILES.get("image")
        description = request.POST.get("description")
        featured = request.POST.get("featured") == "on"
        if image:
            if category.image:
                os.remove(category.image.path)
            category.image = image
        else:
            image = category.image
        category.name = name
        category.description = description
        category.featured = featured
        category.save()

        return redirect("category.index")
def delete_category(request, category_id):
    try:
        category = get_object_or_404(Category, pk=category_id)
        # xóa ảnh nếu có
        image_path = os.path.join(settings.MEDIA_ROOT, str(category.image))
        if os.path.exists(image_path):
            os.remove(image_path)
        category.delete()
        return redirect("category.index")
    except Http404:
        return HttpResponseRedirect(reverse('Category_not_found'))

def user_view(request):
    users = User.objects.all()
    return render(request, 'admin/user/index.html',context={'users':users})

def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    return redirect("user.index")


#### CART ####
@login_required
def cart_view(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)
    return render(request, 'cart.html', context={'cart_items': cart_items})

@login_required
def add_to_cart(request, product_id):
    user = request.user
    product = get_object_or_404(Product, pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("cart")

@login_required
def checkout(request):
    user = request.user
    full_name = request.POST.get("full_name")
    address = request.POST.get("address")
    phone = request.POST.get("phone")

    # Tạo đơn hàng mới
    order = Order.objects.create(
        user=user,
        full_name=full_name,
        address=address,
        phone=phone,
        total_amount=0  # Sẽ cập nhật giá trị sau
    )

    # Lấy danh sách các mục trong giỏ hàng của người dùng
    cart_items = CartItem.objects.filter(user=user)

    # Thêm các mục từ giỏ hàng vào đơn hàng
    for cart_item in cart_items:
        order_item = OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        order_item.save()

    # Tính tổng số tiền của đơn hàng
    total_amount = sum(item.subtotal() for item in order.orderitem_set.all())
    order.total_amount = total_amount
    order.save()

    # Xóa các mục trong giỏ hàng của người dùng
    cart_items.delete()

    return redirect("cart")

def order_completed(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.status = 'Completed'
    order.save()
    return redirect("order.index")

def delete_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.delete()
    return redirect("order.index")