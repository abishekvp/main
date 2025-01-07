from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # auth related urls
    path('', views.index, name='index'),
    path('signup', csrf_exempt(views.signup), name='signup'),
    path('signin', csrf_exempt(views.signin), name='signin'),
    path('signout', csrf_exempt(views.signout), name='signout'),

    path('api/token/', csrf_exempt(views.generate_jwt_token), name='api_token'),


    path('add-user', csrf_exempt(views.add_user), name='add_user'),
    path('get-user', csrf_exempt(views.get_user), name='get_user'),
    path('update-user', csrf_exempt(views.update_user), name='update_user'),
    path('delete-user', csrf_exempt(views.delete_user), name='delete_user'),

    # add call log
    path('add-call-log', csrf_exempt(views.add_call_log), name='add_call_log'),
    path('fetch-call-log', views.fetch_call_log, name='fetch-call-log'),

    # view
    path('view-call-log', views.view_call_log, name='view_call_log'),
]
