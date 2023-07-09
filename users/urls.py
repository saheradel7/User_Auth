from django.contrib import admin
from django.urls import path
from .views import RegisterView, loginView,UserView,logout
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', loginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', logout.as_view()),
]