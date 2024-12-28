from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # auth related urls
    path('signup', csrf_exempt(views.signup), name='signup'),
    path('signin', csrf_exempt(views.signin), name='signin'),
    path('signout', csrf_exempt(views.signout), name='signout'),

    # user related urls
    path('add-user', csrf_exempt(views.add_user), name='add_user'),
    path('get-user', csrf_exempt(views.get_user), name='get_user'),
    path('update-user', csrf_exempt(views.update_user), name='update_user'),
    path('delete-user', csrf_exempt(views.delete_user), name='delete_user'),
]
