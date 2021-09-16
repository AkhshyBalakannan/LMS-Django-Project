'''Custom 404 page view'''
from django.shortcuts import render
from django.template import RequestContext


def custom_page_not_found_view(request, exception):
    return render(request, "organization/404.html", {})
