from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes

from .serializers import (
    UserSignupSerializer,
    UserViewSerializer
)
from .models import CustomUser


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    try:
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': "Sigup Successfully", 'data': serializer.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(str(e))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_detail(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    try:
        serializer = UserViewSerializer(user)
        return Response(serializer.data)
    except Exception as e:
        print(str(e))
        return Response({'message': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def add_staff_under_owner(request):

    try:
        if not request.user.is_owner:
            return Response({'message':"You don't have sufficient permission to perform this action."}, status=status.HTTP_401_UNAUTHORIZED)
        
        if CustomUser.objects.filter(email=request.data.get('email')).exists():
            return Response({'message': f"Please try with different email. User with '{request.data.get('email')}' already exists."}, status=400)
        

        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': "User added successfully", 'user': serializer.data}, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(str(e))
        return Response({'message': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


