from django.urls import path
from .views import get_friend_requests, create_friend_requests, get_pending_friend_requests_by_sender

urlpatterns = [
	path("friend_requests/", get_friend_requests, name="get_friend_requests"),
	path("friend_requests/create/", create_friend_requests, name="create_friend_requests"),
	path("friend_requests/pending/<int:sender_id>/", get_pending_friend_requests_by_sender, name="get_pending_friend_requests_by_sender")
	
]
