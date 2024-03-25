from django.contrib import admin
from django.urls import path,include
from .views import RegisterView,LoginView,UserView,LogoutView
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet
from .views import TeacherViewSet
from .views import ClassViewSet
from . import views

Student_router = DefaultRouter()
Student_router.register(r'students', StudentViewSet, basename='student')

Teacher_router = DefaultRouter()
Teacher_router.register(r'teachers', TeacherViewSet, basename='teacher')

Class_router = DefaultRouter()
Class_router.register(r'classes', ClassViewSet, basename='class')


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserView.as_view(), name='user_profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(Student_router.urls)),
    path('', include(Teacher_router.urls)),
    path('', include(Class_router.urls)),
    path('database_seeding/', views.Seeder , name='seeding'),
    path('database_delete/', views.delete_all , name='delete_all'),

]

