from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FriendRequest
from .serializer import FriendRequestSerializer

@api_view(['GET'])
def get_friend_requests(request):
	friend_requests = FriendRequest.objects.all()
	serializer = FriendRequestSerializer(friend_requests, many=True)
	return Response(serializer.data)

@api_view(['POST'])
def create_friend_requests(request):
	serializer = FriendRequestSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
