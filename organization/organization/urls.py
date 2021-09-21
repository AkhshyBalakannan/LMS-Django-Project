'''Projects URL'''
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from users import views as user_views
from leavemanagementsys import views as lms_views
from organization import views as org_views

# All views from apps are imported with app_views and used
urlpatterns = [
    path('', user_views.home, name='default'),
    path('login/', auth_views.LoginView.as_view(
         template_name='registration/login.html'), name='login'),
    path('home/', user_views.home, name='home'),
    path('myleave/', user_views.profile, name='myleave'),
    path('user-profile/', user_views.user_profile, name='user-profile'),
    path('leaveRequest/', lms_views.request_leave, name='leave-request'),
    path('cancelRequest/', lms_views.ViewListCancelRequest.as_view(),
         name='cancel-request'),
    path('leaveRespond/', lms_views.ViewListLeaveRequest.as_view(),
         name='list-leave-respond'),
    path('userleaveRespond/<int:pk>/', lms_views.ViewDetailLeaveRequest.as_view(),
         name='detail-leave-respond'),
    path('userleaveRespond/<str:user_first_name>/<int:leaverequest>/',
         lms_views.ViewListUserLeaves.as_view(), name='detail-user-leaves'),
    path('employeeleave/', lms_views.search_employee, name='search-employee'),
    path('userleaveRespond/<str:user_email_id>/',
         lms_views.ViewListEmployeeLeaves.as_view(), name='employee-leaves'),
    path('logout/', auth_views.LogoutView.as_view(
         template_name='registration/logout.html'), name='logout'),
    path('reset-mypass/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html'), name='password_reset'),
    path('reset-mypass/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset-mypass-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset-mypass-completed/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_completed.html'), name='password_reset_complete'),
    path('register/', user_views.register, name='register-user'),
    path('select-update-user/', user_views.select_update_user,
         name='select-update-user'),
    path('update-user/<str:email>/',
         user_views.update_user, name='update-user'),
    path('admin/', admin.site.urls),
]

handler404 = org_views.custom_page_not_found_view


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
