'''Custom Middleware to check admin and manager privilege'''
from django.shortcuts import render


def privilege_check(get_response):

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = get_response(request)
        link = request.get_full_path()
        if request.user.is_authenticated:
            if link in ('/select-update-user/', '/register/') or not link.find('update-user') == -1:
                if not request.user.groups.filter(name='Adminstrator').exists():
                    return render(request, 'base/unauth.html', status=401)

            elif link == '/leaveRespond/' or not link.find('userleaveRespond') == -1:
                if not request.user.is_manager:
                    return render(request, 'base/unauth.html', status=401)
        return response

    return middleware
