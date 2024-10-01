import stripe
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user.api.serializers import UserRegisterSerializer, UserSerializer, UserUpdateSerializer, UserPublicSerializer
from user.models import User
from wallet.models import Wallet
import os
from dotenv import load_dotenv

load_dotenv()
stripe_key = os.getenv('STRIPE_BACKEND_ID')
stripe.api_key = stripe_key


class RegisterView(APIView):
    def post(self, request):
        wallet = Wallet(balance=0)
        wallet.save()

        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            new_user = serializer.save()
            emailUser = serializer.data['email']

            user_stripe = stripe.Customer.create(email=emailUser)
            id_user_stripe = user_stripe.id

            user = User.objects.get(pk=new_user.id)
            user.id_user_stripe = id_user_stripe
            user.wallet = wallet

            user.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def put(self, request):
        if 'password' in request.data:
            password = request.data['password']
            request.data['password'] = make_password(password)
        
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersPublic(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.query_params.get('search', None)

        if search_query:
            users = User.objects.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        else:
            users = User.objects.all()

        serializer = UserPublicSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserByIdPublic(APIView):
    parser_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserPublicSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': "El usuario no existe"}, status=status.HTTP_404_NOT_FOUND)