"""
Django views for resident_advisor project.

"""

from .helpers import has_model_permissions
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from resident_advisor.apps.call_tree.models import RACallProfile, RACallTree
from resident_advisor.apps.call_tree.forms import RACallProfileForm, RACallTreeForm
from resident_advisor.libs.users.managers import UserManager
from resident_advisor.libs.users.forms import UserCreationForm, UserEditForm


@login_required
def home(request):
    """    Display the Landing Page    """

    context = {}

    return render(request, 'home.html', context)

@login_required
def call_tree_home(request):

    filter_kwargs = {}

    if not request.user.is_superuser:
        filter_kwargs['owners__in'] = [request.user, ]

    phone_trees = RACallTree.objects.filter(**filter_kwargs)

    if phone_trees.count() == 1:
        # The User Can Only View One Phone Tree
        phone_tree = phone_trees[0]

        # Redirect User to More Appropriate View Page
        return redirect('call_tree_view', call_tree_id=phone_tree.pk)

    context = {
        'trees': phone_trees,
    }

    return render(request, 'call_tree_home.html', context)

@login_required
def call_tree_new(request):

    form = RACallTreeForm(data=request.POST or None, files=request.FILES or None)

    if form.is_valid():
        location_redirect = form.save()
        return redirect(**location_redirect)

    context = {
        'form': form
    }

    return render(request, 'call_tree_new.html', context)

@login_required
def call_tree_view(request, call_tree_id=None):
    """    Display the Landing Page    """

    profiles = RACallProfile.objects.all()

    context = {
        "profiles": profiles,
    }

    if has_model_permissions(request.user, RACallTree, 'change', 'call_tree'):
        template = 'call_tree_view_admin.html'
    else:
        template = 'call_tree_view.html'

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

    manager = UserManager()

    if request.POST:
        if '_bulkactions' in request.POST:

            items = []
            for item in request.POST.getlist('_selected_action'):
                item = User.objects.get(pk=int(item))
                items.append(item)

            manager.process_bulk_actions(action=request.POST['action'], queryset=items)

    users = User.objects.all()

    context = {
        'users': users,
        "actions": manager.bulk_actions ,
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