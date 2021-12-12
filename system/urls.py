
"""system URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clubs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('sign_up/', views.sign_up, name = 'sign_up'),
    path('log_in/', views.log_in, name = 'log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('clubs/', views.clubs, name = 'clubs'),
    path('profile/', views.profile, name='profile'),
    path('password/', views.password, name='password'),
    path('profile/clubs/', views.profile_clubs, name='profile_clubs'),
    path('club/<int:club_id>', views.show_club, name='show_club'),
    path('club_creator/', views.club_creator, name = 'club_creator'),
    path('club/<int:club_id>/memberlist', views.club_member_list, name = 'club_member_list'),
    path('club/<int:club_id>/memberlist/<userid>/<str:action>/', views.club_member_list_action, name = 'club_member_list_action'),
    path('member/<userid>', views.member_id, name = 'member<userid>'),
    path('tournaments/', views.tournaments, name = 'tournaments'),
]
