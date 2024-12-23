from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, update_session_auth_hash, logout
from .forms import CreateUserForm, LoginForm
from .models import Hobby
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import json
from datetime import datetime


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})


def homepage(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/homepage.html')

def homepage(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('dashboard') 
    return render(request, 'api/homepage.html')

def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('')


def register(request: HttpRequest) -> HttpResponse:
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    context = {'registerform': form}
    return render(request, 'api/register.html', context=context)


def login(request: HttpRequest) -> HttpResponse:
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
    context = {'loginform': form}
    return render(request, 'api/login.html', context=context)


@login_required
def profile(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        user = request.user
        profile_data = {
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d') if user.date_of_birth else ''
        }
        return JsonResponse(profile_data)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = request.user
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
            date_of_birth = data.get('date_of_birth')
            user.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            user.save()
            return JsonResponse({'message': 'Profile updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@login_required
def update_password(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        data = json.loads(request.body)
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        user = request.user

        if not user.check_password(current_password):
            return JsonResponse({'error': 'Current password is incorrect.'}, status=400)
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return JsonResponse({'error': e.messages}, status=400)

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        return JsonResponse({'message': 'Password updated successfully.'})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


@login_required
def user_hobbies(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        user = request.user
        hobbies = user.hobbies.all()
        hobbies_data = [
            {"id": hobby.id, "name": hobby.name} for hobby in hobbies
        ]
        return JsonResponse(hobbies_data, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=405)  


@login_required
def all_hobbies(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        hobbies = Hobby.objects.all()
        hobbies_data = [
            {"id": hobby.id, "name": hobby.name} for hobby in hobbies
        ]
        return JsonResponse(hobbies_data, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def delete_hobby(request: HttpRequest, hobby_id: int) -> JsonResponse:
    if request.method == 'DELETE': 
        try:
            hobby = request.user.hobbies.get(id=hobby_id)
            request.user.hobbies.remove(hobby)
            return JsonResponse({'message': 'Hobby deleted successfully'}, status=200)
        except Hobby.DoesNotExist:
            return JsonResponse({'error': 'Hobby not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def create_hobby(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        if name:
            hobby = Hobby.objects.create(name=name)
            return JsonResponse({"id": hobby.id, "name": hobby.name}, status=201)
        return JsonResponse({"error": "Invalid data"}, status=400)
    return JsonResponse({"error": "Invalid method"}, status=405)


@login_required
def add_hobby(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        data = json.loads(request.body)
        hobby_id = data.get("hobby_id")
        if hobby_id:
            hobby = Hobby.objects.get(id=hobby_id)
            request.user.hobbies.add(hobby)
            return JsonResponse({"message": "Hobby added successfully"}, status=200)
        return JsonResponse({"error": "Hobby ID is required"}, status=400)
    return JsonResponse({"error": "Invalid method"}, status=405)