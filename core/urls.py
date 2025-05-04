

from django.urls import path
from .views import LoginView, ProfileView, signup_view, dashboard_view,RegisterView

urlpatterns = [
    path('login/', LoginView.as_view(), name='api-login'),
    path('register/', RegisterView.as_view(), name='register'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('signup/', signup_view, name='signup'),
    path('dashboard/', dashboard_view, name='dashboard'),
]