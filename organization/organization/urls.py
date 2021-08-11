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
    path('profile/', login_required(user_views.ViewListProfile.as_view()), name='profile'),
    path('leaveRequest/', lms_views.request_leave, name='leave-request'),
    path('cancelRequest/', lms_views.cancel_request, name='cancel-request'),
    path('leaveRespond/', login_required(lms_views.ViewListLeaveRequest.as_view()),
         name='list-leave-respond'),
    path('userleaveRespond/<int:pk>/', login_required(lms_views.ViewDetailLeaveRequest.as_view()),
         name='detail-leave-respond'),
    path('userleaves/<str:user_first_name>/<int:leaverequest>/',
         login_required(lms_views.ViewListUserLeaves.as_view()), name='detail-user-leaves'),
    path('leaveRespond/update/<int:pk>/',
         lms_views.leave_request_process, name='update-leave-respond'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('reset-mypass/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html'), name='password_reset'),
    path('reset-mypass/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset-mypass-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset-mypass-completed/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_completed.html'), name='password_reset_complete'),
    path('register/', user_views.register, name='register-user'),
    path('admin/', admin.site.urls),
]
