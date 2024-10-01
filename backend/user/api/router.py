from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from user.api.views import RegisterView, UserMeView, UsersPublic, UserByIdPublic

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('user/me/', UserMeView.as_view()),
    path('users/get_all/', UsersPublic.as_view()),
    path('users/get_all/<int:user_id>/', UserByIdPublic.as_view()),
]
