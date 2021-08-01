from django.contrib import admin
from django.contrib.auth import views as auth_views
from users import views as user_views
from leavemanagementsys import views as lms_views
from django.urls import path

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('home/', user_views.home, name='home'),
    path('profile/', user_views.profile, name='profile'),
    path('leaveRequest/', lms_views.request_leave, name='leave-request'),
    path('cancelRequest/', lms_views.cancel_request, name='cancel-request'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', user_views.register, name='register-employee'),
    path('admin/', admin.site.urls),
]
