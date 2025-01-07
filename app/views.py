import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

# Create your views here.
def index(request):

    return render(request, 'index.html')

def signup(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    if not username or not email or not password:
        return JsonResponse({'status': 400, 'message': 'Missing parameters'})
    if User.objects.filter(Q(username=username) | Q(email=email)).exists():
        return JsonResponse({'status': 403, 'message': 'User already exists'})
    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()
    return JsonResponse({'status': 200, 'message': 'User created'})


def signin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'status': 200, 'message': 'User logged in'})
    return JsonResponse({'status': 403, 'message': 'Invalid credentials'})


def signout(request):
    logout(request)
    return JsonResponse({'status': 200, 'message': 'User logged out'})


def add_user(request):
    from app.models import UserData
    username = request.POST.get('username')
    email = request.POST.get('email')
    contact = request.POST.get('contact')
    password = request.POST.get('password')
    if not username or not email or not contact or not password:
        return JsonResponse({'status': 400, 'message': 'Missing parameters'})
    if UserData.objects.filter(Q(username=username) | Q(email=email) | Q(contact=contact)).exists():
        return JsonResponse({'status': 403, 'message': 'User already exists'})
    UserData.objects.create(username=username, email=email, contact=contact, password=password)
    return JsonResponse({'status': 200, 'message': 'User created'})


def get_user(request):
    from app.models import UserData
    username = request.GET.get('username')
    email = request.GET.get('email')
    contact = request.GET.get('contact')
    if not username and not email and not contact:
        return JsonResponse({'status': 400, 'message': 'Missing parameters'})
    user = UserData.objects.filter(Q(username=username) | Q(email=email) | Q(contact=contact)).first()
    if not user:
        return JsonResponse({'status': 404, 'message': 'User not found'})
    data = {'username': user.username, 'email': user.email, 'contact': user.contact, 'active': user.is_active, 'created_at': user.created_at, 'updated_at': user.updated_at}
    return JsonResponse({'status': 200, 'message': 'User found', 'data': data})


def update_user(request):
    from app.models import UserData
    username = request.POST.get('username')
    email = request.POST.get('email')
    contact = request.POST.get('contact')
    password = request.POST.get('password')
    if not username or not email or not contact or not password:
        return JsonResponse({'status': 400, 'message': 'Missing parameters'})
    user = UserData.objects.filter(Q(username=username) | Q(email=email) | Q(contact=contact)).first()
    if not user:
        return JsonResponse({'status': 404, 'message': 'User not found'})
    if username and username != user.username:
        user.username = username
    if email and email != user.email:
        user.email = email
    if contact and contact != user.contact:
        user.contact = contact
    if password:
        if password != user.password:
            user.password = password
        elif password == user.password:
            return JsonResponse({'status': 400, 'message': 'Password is same as before'})
    user.save()
    return JsonResponse({'status': 200, 'message': 'User updated'})

def delete_user(request):
    from app.models import UserData
    username = request.POST.get('username')
    email = request.POST.get('email')
    contact = request.POST.get('contact')
    if not username and not email and not contact:
        return JsonResponse({'status': 400, 'message': 'Missing parameters'})
    user = UserData.objects.filter(Q(username=username) | Q(email=email) | Q(contact=contact)).first()
    if not user:
        return JsonResponse({'status': 404, 'message': 'User not found'})
    user.delete()
    return JsonResponse({'status': 200, 'message': 'User deleted'})


from rest_framework_simplejwt.tokens import AccessToken

def generate_jwt_token(user):
    # Generate JWT token for the given user
    token = AccessToken.for_user(user)
    return token


@csrf_exempt
def add_call_log(request):
    from app.models import CallLog
    from_number = request.POST.get('from_number')
    to_number = request.POST.get('to_number')
    status = request.POST.get('status')
    if not from_number or not to_number or not status:
        return JsonResponse({'status': 400, 'message': 'Missing parameters'})
    CallLog.objects.create(from_number=from_number, to_number=to_number, status=status)
    return JsonResponse({'status': 200, 'message': 'Call log added'})


def view_call_log(request):
    return render(request, 'call-log.html')


def fetch_call_log(request):
    from app.models import CallLog
    call_logs = CallLog.objects.all()
    logs = []
    for call_log in call_logs:
        logs.append({'from_number': call_log.from_number, 'to_number': call_log.to_number, 'status': call_log.status})
    return JsonResponse({'status': 200, 'logs': logs})