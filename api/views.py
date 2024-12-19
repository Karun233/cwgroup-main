from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout as auth_logout, update_session_auth_hash
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import json
from datetime import datetime

from .forms import CreateUserForm, LoginForm
from .models import Hobby


def main_spa(request: HttpRequest) -> HttpResponse:
    # Renders the main SPA page for authenticated users
    return render(request, 'api/spa/index.html')


def homepage_view(request: HttpRequest) -> HttpResponse:
    # Displays a homepage. If authenticated, redirects user to the dashboard.
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'api/homepage.html')


def logout_user(request: HttpRequest) -> HttpResponse:
    # Logs the user out and returns them to the homepage (or login page).
    auth_logout(request)
    return redirect('')


def register_user(request: HttpRequest) -> HttpResponse:
    registration_form = CreateUserForm()
    if request.method == "POST":
        registration_form = CreateUserForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            return redirect('login')
        else:
            # Print the validation errors in the terminal
            print("Form errors:", registration_form.errors)
    return render(request, 'api/register.html', {'registerform': registration_form})




def login_user(request: HttpRequest) -> HttpResponse:
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print(f"User {user.username} has just logged in.")  # Console message
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid username or password.')
    return render(request, 'api/login.html', {'loginform': form})



@login_required
def user_profile(request: HttpRequest) -> JsonResponse:
    # Handles retrieval and updating of the user's profile data.
    if request.method == 'GET':
        current_user = request.user
        profile_info = {
            'username': current_user.username,
            'name': current_user.name,
            'email': current_user.email,
            'date_of_birth': current_user.date_of_birth.strftime('%Y-%m-%d') if current_user.date_of_birth else ''
        }
        return JsonResponse(profile_info)

    elif request.method == 'POST':
        try:
            payload = json.loads(request.body)
            current_user = request.user
            current_user.name = payload.get('name', current_user.name)
            current_user.email = payload.get('email', current_user.email)
            dob_str = payload.get('date_of_birth')
            if dob_str:
                current_user.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
            current_user.save()
            return JsonResponse({'message': 'Profile successfully updated.'})
        except Exception as exc:
            return JsonResponse({'error': str(exc)}, status=400)

    return JsonResponse({'error': 'Unsupported HTTP method.'}, status=405)


@login_required
def change_password(request: HttpRequest) -> JsonResponse:
    # Updates the user's password, ensuring the current password is correct and the new one is valid.
    if request.method == 'POST':
        payload = json.loads(request.body)
        old_password = payload.get('current_password')
        new_password = payload.get('new_password')
        current_user = request.user

        if not current_user.check_password(old_password):
            return JsonResponse({'error': 'The provided current password is incorrect.'}, status=400)

        try:
            validate_password(new_password, current_user)
        except ValidationError as e:
            return JsonResponse({'error': e.messages}, status=400)

        current_user.set_password(new_password)
        current_user.save()
        update_session_auth_hash(request, current_user)
        return JsonResponse({'message': 'Password changed successfully.'})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


@login_required
def retrieve_user_hobbies(request: HttpRequest) -> JsonResponse:
    # Returns a list of hobbies associated with the logged-in user.
    if request.method == 'GET':
        current_user = request.user
        user_hobby_list = current_user.hobbies.all()
        formatted_hobbies = [{"id": h.id, "name": h.name} for h in user_hobby_list]
        return JsonResponse(formatted_hobbies, safe=False)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def list_all_hobbies(request: HttpRequest) -> JsonResponse:
    # Returns a list of all hobbies available in the database.
    if request.method == 'GET':
        all_hobby_qs = Hobby.objects.all()
        all_hobby_data = [{"id": h.id, "name": h.name} for h in all_hobby_qs]
        return JsonResponse(all_hobby_data, safe=False)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def remove_user_hobby(request: HttpRequest, hobby_id: int) -> JsonResponse:
    # Removes a specific hobby from the user's hobby list.
    if request.method == 'DELETE':
        current_user = request.user
        try:
            hobby_to_remove = current_user.hobbies.get(id=hobby_id)
            current_user.hobbies.remove(hobby_to_remove)
            return JsonResponse({'message': 'Hobby has been successfully removed.'}, status=200)
        except Hobby.DoesNotExist:
            return JsonResponse({'error': 'No matching hobby found.'}, status=404)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@login_required
def create_new_hobby(request: HttpRequest) -> JsonResponse:
    # Creates a new hobby record in the database.
    if request.method == "POST":
        payload = json.loads(request.body)
        hobby_name = payload.get("name")
        if hobby_name:
            new_hobby = Hobby.objects.create(name=hobby_name)
            return JsonResponse({"id": new_hobby.id, "name": new_hobby.name}, status=201)
        return JsonResponse({"error": "Hobby name is required."}, status=400)

    return JsonResponse({"error": "Method not allowed."}, status=405)


@login_required
def add_user_hobby(request: HttpRequest) -> JsonResponse:
    # Associates an existing hobby with the current user.
    if request.method == "POST":
        payload = json.loads(request.body)
        hobby_id = payload.get("hobby_id")
        if hobby_id:
            try:
                hobby_instance = Hobby.objects.get(id=hobby_id)
                request.user.hobbies.add(hobby_instance)
                return JsonResponse({"message": "Hobby successfully added."}, status=200)
            except Hobby.DoesNotExist:
                return JsonResponse({"error": "Hobby not found."}, status=404)
        return JsonResponse({"error": "Hobby ID not provided."}, status=400)

    return JsonResponse({"error": "Method not allowed."}, status=405)
