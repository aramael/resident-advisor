"""
Django views for resident_advisor project.

"""

from django.shortcuts import render, redirect, get_object_or_404
from resident_advisor.apps.call_tree.models import RACallProfile
from resident_advisor.apps.call_tree.forms import RACallProfileForm


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


def call_tree_proflie(request):
    """    Display the Landing Page    """

    profile = get_object_or_404(RACallProfile, user=request.user)

    form = RACallProfileForm(instance=profile, data=request.POST or None, files=request.FILES or None)

    if form.is_valid():
        location_redirect = form.save()
        return redirect(**location_redirect)

    context = {
        "profile": profile,
        "form": form,
    }

    return render(request, 'call_tree_profile.html', context)