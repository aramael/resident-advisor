"""
Django views for resident_advisor project.

"""

from .helpers import has_model_permissions
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from resident_advisor.apps.call_tree.models import RACallProfile
from resident_advisor.apps.call_tree.forms import RACallProfileForm, UserCreationForm, UserEditForm


@login_required
def home(request):
    """    Display the Landing Page    """

    context = {}

    return render(request, 'home.html', context)

@login_required
def call_tree_home(request):
    """    Display the Landing Page    """

    profiles = RACallProfile.objects.all()

    context = {
        "profiles": profiles,
    }

    if has_model_permissions(request.user, RACallProfile, 'edit', 'call_tree'):
        template = 'call_tree_home.html'
    else:
        template = 'call_tree_home_admin.html'

    return render(request, template, context)


@login_required
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

#==============================================================================
# Users Pages
#==============================================================================


def users_home(request):

    users = User.objects.all()

    context = {
        'users': users,
    }

    return render(request, 'users_home.html', context)


def users_new(request):

    form = UserCreationForm(data=request.POST or None, files=request.FILES or None)

    if form.is_valid():
        location_redirect = form.save()
        return redirect(**location_redirect)

    context = {
        'form': form,
    }

    return render(request, 'users_new.html', context)


def users_edit(request, user_id=None, self_edit=False):

    if self_edit:
        user = request.user
    else:
        user = get_object_or_404(User, pk=user_id)

    form = UserEditForm(instance=user, data=request.POST or None, files=request.FILES or None)

    if form.is_valid():
        location_redirect = form.save()
        return redirect(**location_redirect)

    context = {
        'form': form
    }

    return render(request, 'users_edit.html', context)