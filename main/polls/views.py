from itertools import product

from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Userprofile, Product, Order


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        try:
            user_profile = Userprofile.objects.get(user = request.user)  # Получаем профиль текущего пользователя
            orders = Order.objects.filter(user = request.user)
        except Userprofile.DoesNotExist:
            user_profile = None  # Профиль не существует
        return render(request, 'index.html', {'user_profile': user_profile, 'orders': orders})

    return render(request, 'index.html', )


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Пользователь уже существует'})

        if password != password2:
            return render(request, 'register.html', {'error': 'Пароли не совпадают'})

        try:

            user = User.objects.create_user(username=username, password=password)

            Userprofile.objects.create(user=user, first_name=first_name, last_name=last_name, middle_name=middle_name)
            return redirect('login')
        except IntegrityError:
            return render(request, 'register.html', {'error': 'Ошибка создания пользователя'})

    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'errors': 'Такого пользователя не существует'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        try:
            Product.objects.create(title=title, description=description)
        except IntegrityError:
            return render(request, 'create_post.html', {'error': 'Ошибка создания продукта'})
    return render(request, 'create_post.html')


def list_post(request):
    query = request.GET.get('query', '')
    posts = Product.objects.all()

    if query:
        posts = posts.filter(title__icontains=query)
        posts = posts.filter(description__icontains=query)

    return render(request, 'post_list.html', {'posts': posts, 'query': query})


def post_detail(request, post_id):
    product = get_object_or_404(Product, id=post_id)

    if request.method == 'POST':
        Order.objects.create(user = request.user, product = product)
    return render(request, 'post_detail.html', {'post': product})


def edit_profile(request):
    user_profile = request.user.userprofile  # Получаем профиль текущего пользователя
    user = request.user

    if request.method == 'POST':
        # Получаем данные из формы
        username = request.POST.get('username', user.username)
        first_name = request.POST.get('first_name', user_profile.first_name)
        email = request.POST.get('email', user.email)

        # Проверка уникальности имени пользователя

        # Обновляем данные пользователя
        user.username = username
        user_profile.first_name = first_name
        user.email = email

        # Обработка загрузки аватара
        if request.FILES.get('avatar'):
            user_profile.avatar = request.FILES['avatar']

        user.save()  # Сохраняем изменения пользователя
        user_profile.save()  # Сохраняем изменения профиля

        return redirect('home')  # Перенаправляем на страницу профиля


    return render(request, 'edit_profile.html', {'user_profile': user_profile})
