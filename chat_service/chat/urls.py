from django.urls import path
from .views import get_friend_requests, create_friend_requests

urlpatterns = [
	path("friend_requests/", get_friend_requests, name="get_friend_requests"),
	path("friend_requests/create/", create_friend_requests, name="create_friend_requests")
]
