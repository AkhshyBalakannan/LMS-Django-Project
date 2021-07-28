from django.contrib import admin
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('lms/', include('leaveManagementSys.urls')),
    path('signup/', user_views.register, name='signup-user'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('admin/', admin.site.urls),
]
