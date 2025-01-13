from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, update_session_auth_hash, logout
from .forms import CreateUserForm, LoginForm
from .models import Hobby, FriendRequest, CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import json
from datetime import datetime
from django.views.decorators.http import require_GET, require_POST
from typing import Any
from django.core.paginator import Paginator
from django.db.models import Count, Q


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
            if date_of_birth:
                user.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            user.save()
            return JsonResponse({'message': 'Profile updated successfully'})
        except Exception as e:
            logger.error(f"Error in /api/profile POST: {e}")
            return JsonResponse({'error': str(e)}, status=400)

    logger.error("Invalid request method for /api/profile/")
    return JsonResponse({'error': 'Invalid request method'}, status=405)


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


import logging
logger = logging.getLogger(__name__)

@login_required
def all_hobbies(request: HttpRequest) -> JsonResponse:
    try:
        if request.method == 'GET':
            hobbies = Hobby.objects.all()
            hobbies_data = [{"id": hobby.id, "name": hobby.name} for hobby in hobbies]
            return JsonResponse(hobbies_data, safe=False)
        logger.error("Invalid request method for /api/all-hobbies/")
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    except Exception as e:
        logger.error(f"Error in /api/all-hobbies/: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


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




@login_required
@require_POST
def send_friend_request(request):
    """
    Handles sending a friend request via AJAX (POST).
    """
    try:
        data = json.loads(request.body)
        receiver_id = data.get("receiver_id")
        if not receiver_id:
            return JsonResponse({"error": "Receiver ID is required"}, status=400)

        from django.contrib.auth import get_user_model
        CustomUser = get_user_model()

        receiver = CustomUser.objects.get(id=receiver_id)

        # Prevent duplicate friend requests
        if FriendRequest.objects.filter(sender=request.user, receiver=receiver).exists():
            return JsonResponse({"error": "Friend request already sent"}, status=400)

        # Prevent sending requests to already-friends
        if receiver in request.user.friends.all():
            return JsonResponse({"error": "User is already your friend"}, status=400)

        # Create the friend request
        FriendRequest.objects.create(sender=request.user, receiver=receiver)
        return JsonResponse({"message": "Friend request sent successfully"})
    
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
@require_POST
def manage_friend_request(request, request_id):
    """
    Handles accepting or declining a friend request via AJAX (POST).
    """
    try:
        data = json.loads(request.body)
        action = data.get("action")
        
        friend_request = FriendRequest.objects.get(id=request_id, receiver=request.user)
        if action == "accept":
            # Add as friends
            request.user.friends.add(friend_request.sender)
            friend_request.sender.friends.add(request.user)

            friend_request.delete()  # remove the FriendRequest record
            return JsonResponse({"message": "Friend request accepted"})
        
        elif action == "decline":
            friend_request.delete()
            return JsonResponse({"message": "Friend request declined"})
        
        return JsonResponse({"error": "Invalid action"}, status=400)
    
    except FriendRequest.DoesNotExist:
        return JsonResponse({"error": "Friend request not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
@require_GET
def get_friend_requests(request):
    """
    Fetches the friend requests for the logged-in user (receiver).
    """
    try:
        friend_requests = FriendRequest.objects.filter(receiver=request.user)
        data = [
            {
                "id": fr.id,
                "sender": {
                    "id": fr.sender.id,
                    "username": fr.sender.username,
                },
                "status": fr.status,  # if your model has a 'status' field
            }
            for fr in friend_requests
        ]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@login_required
@require_GET
def get_friends(request):
    """
    Fetches the list of friends for the logged-in user (via AJAX GET).
    """
    try:
        user_friends = request.user.friends.all()
        data = [
            {"id": friend.id, "username": friend.username}
            for friend in user_friends
        ]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@login_required
def get_users(request):
    search_query = request.GET.get("search", "").strip()
    
    # Get all users, excluding the currently logged-in user
    users = CustomUser.objects.exclude(id=request.user.id)

    # Apply search filter if a search query is provided
    if search_query:
        users = users.filter(username__icontains=search_query)

    # Prepare the data to return
    users_data = list(users.values("id", "username", "name", "email"))

    return JsonResponse(users_data, safe=False)


@login_required
def similar_hobbies(request):
    # Get the current user's hobby IDs
    user_hobbies = request.user.hobbies.values_list('id', flat=True)

    # Get query parameters for age filters
    min_age_str = request.GET.get('age_min', '')
    max_age_str = request.GET.get('age_max', '')

    # Convert them to integers if possible
    min_age = int(min_age_str) if min_age_str.isdigit() else None
    max_age = int(max_age_str) if max_age_str.isdigit() else None

    # Build a base queryset
    users = (
        CustomUser.objects
        .exclude(id=request.user.id)  # Exclude current user
        .annotate(
            common_hobbies=Count('hobbies', filter=Q(hobbies__id__in=user_hobbies))
        )
    )

    # Build date filters (for age)
    # For demonstration, we use the year 2025 - age as a rough DOB cutoff.
    date_filters = {}
    if min_age is not None:
        # People must be at least `min_age` ⇒ Born on or before (2025 - min_age).
        date_filters['date_of_birth__lte'] = f'{2025 - min_age}-01-01'
    if max_age is not None:
        # People must be at most `max_age` ⇒ Born on or after (2025 - max_age).
        date_filters['date_of_birth__gte'] = f'{2025 - max_age}-01-01'

    if date_filters:
        users = users.filter(**date_filters)

    # Order by number of common hobbies desc, then by name asc
    users = users.order_by('-common_hobbies', 'name')

    # Handle pagination
    page_num = request.GET.get('page', 1)
    paginator = Paginator(users, 10)
    page_obj = paginator.get_page(page_num)

    # Build user data array
    user_data = []
    for u in page_obj:
        dob_year = u.date_of_birth.year if u.date_of_birth else None
        age = 2025 - dob_year if dob_year else None

        user_data.append({
            'id': u.id,
            'name': u.name,
            'common_hobbies': u.common_hobbies,
            'age': age,
        })

    # Debug prints in your server logs
    print(f"Request Parameters: min_age={min_age}, max_age={max_age}, page={page_num}")
    print(f"Total Users in Queryset (after filters): {users.count()}")
    print(f"Users on this Page: {[user.id for user in page_obj]}")
    print("User Data in Response:", user_data)

    return JsonResponse({
        'users': user_data,
        'page': page_obj.number,
        'pages': paginator.num_pages,
    })
