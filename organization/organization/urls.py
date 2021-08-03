from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from users import views as user_views
from leavemanagementsys import views as lms_views
from django.urls import path

urlpatterns = [
    path('', user_views.home, name='default'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('home/', user_views.home, name='home'),
    path('profile/', user_views.profile, name='profile'),
    path('leaveRequest/', lms_views.request_leave, name='leave-request'),
    path('cancelRequest/', lms_views.cancel_request, name='cancel-request'),
    path('leaveRespond/', login_required(lms_views.ViewListLeaveRequest.as_view()),
         name='list-leave-respond'),
    path('userleaveRespond/<int:pk>/', login_required(lms_views.ViewDetailLeaveRequest.as_view()),
         name='detail-leave-respond'),
    path('userleaveRespond/update/<int:pk>/',
         login_required(lms_views.LeaveRequestUpdate.as_view()),
         name='update-leave-respond'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', user_views.register, name='register-user'),
    path('admin/', admin.site.urls),
]
