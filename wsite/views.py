from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')


#### ADMIN ####
def admin_view(request):
    return render(request, 'admin/index.html')


def product_view(request):
    return render(request, 'admin/product/index.html')

def category_view(request):
    return render(request, 'admin/category/index.html')

def user_view(request):
    return render(request, 'admin/user/index.html')