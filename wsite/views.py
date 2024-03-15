from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from .forms import RegistrationForm
from django.contrib.auth.models import User
######## FRONT-END #######
def index(request):
    return render(request, 'index.html')

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


def product_view(request):
    return render(request, 'admin/product/index.html')

def category_view(request):
    return render(request, 'admin/category/index.html')

def user_view(request):
    return render(request, 'admin/user/index.html')


