from django.urls import path

from events.views import Login

# from events.views import Login


urlpatterns = [
    path(r'user/login/', Login.as_view(), name='user_login'),
]
