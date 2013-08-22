"""
Django views for resident_advisor project.

"""

from django.shortcuts import render
from resident_advisor.apps.call_tree.models import RACallProfile


def home(request):
    """    Display the Landing Page    """

    context = {}

    return render(request, '', context)


def call_tree_home(request):
    """    Display the Landing Page    """

    profiles = RACallProfile.objects.all()

    context = {
        "profiles": profiles,
    }

    return render(request, 'call_tree_home.html', context)