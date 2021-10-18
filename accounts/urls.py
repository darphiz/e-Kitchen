from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_user, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('dashboard/<action>', views.dashboard, name='dashboard'),
    path('add_staff/', views.add_staff, name="add_staff")
]