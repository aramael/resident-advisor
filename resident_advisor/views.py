"""
Django views for resident_advisor project.

"""

from .helpers import has_model_permissions
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from resident_advisor.apps.call_tree.models import RACallProfile, RACallTree
from resident_advisor.apps.call_tree.forms import RACallProfileForm, RACallTreeForm, RACallTreeEditForm
from resident_advisor.libs.users.managers import UserManager
from resident_advisor.libs.users.forms import UserCreationForm, UserEditForm, ProfileCreationForm
from django.db.models import Q


@login_required
def home(request):
    """    Display the Landing Page    """

    context = {}

    return render(request, 'home.html', context)

@login_required
def call_tree_home(request):

    if not request.user.is_superuser:
        phone_trees = RACallTree.objects.filter(Q(owners__in=[request.user, ]) | Q(phone_numbers__in=[request.user.racallprofile, ])).distinct()
    else:
        phone_trees = RACallTree.objects.all()

    if phone_trees.count() == 1:
        # The User Can Only View One Phone Tree
        phone_tree = phone_trees[0]

        # Redirect User to More Appropriate View Page
        return redirect('call_tree_view', call_tree_id=phone_tree.pk)

    context = {
        'trees': phone_trees,
    }

    if has_model_permissions(request.user, 'change', phone_trees):
        template = 'call_tree_home_admin.html'
    else:
        template = 'call_tree_home.html'

    return render(request, template, context)

@login_required
def call_tree_new(request):

    form = RACallTreeForm(initial={'owners': [request.user.pk, ], 'phone_numbers': [request.user.racallprofile.pk, ]},
                          data=request.POST or None,
                          files=request.FILES or None)

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

    phone_tree = get_object_or_404(RACallTree, pk=call_tree_id)

    profiles = phone_tree.phone_numbers.all()

    context = {
        "tree": phone_tree,
        "profiles": profiles,
    }

    if has_model_permissions(request.user, 'change', phone_tree):
        template = 'call_tree_view_admin.html'
    else:
        template = 'call_tree_view.html'

    return render(request, template, context)


@login_required
def call_tree_profile_new(request, call_tree_id=None):
    """    Display the Landing Page    """

    phone_tree = get_object_or_404(RACallTree, pk=call_tree_id)

    if not has_model_permissions(request.user, 'change', phone_tree):
        return HttpResponseForbidden()

    new_profile_form = ProfileCreationForm(data=request.POST or None, files=request.FILES or None)
    add_existing_form = RACallTreeEditForm(instance=phone_tree, data=request.POST or None, files=request.FILES or None)

    if new_profile_form.is_valid():
        location_redirect = new_profile_form.save(phone_tree)
        return redirect(**location_redirect)

    if add_existing_form.is_valid():
        location_redirect = add_existing_form.save(phone_tree)
        return redirect(**location_redirect)

    context = {
        'new_profile_form': new_profile_form,
        'add_existing_form': add_existing_form,
    }

    return render(request, 'call_tree_new_profile.html', context)


@login_required
def call_tree_profile(request, profile_id=None):
    """    Display the Landing Page    """

    if profile_id is not None:
        profile = get_object_or_404(RACallProfile, pk=profile_id)
    else:
        profile = get_object_or_404(RACallProfile, user=request.user)

    if not has_model_permissions(request.user, 'change', profile):
        return HttpResponseForbidden()

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

@login_required
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

@login_required
def users_new(request):

    form = UserCreationForm(data=request.POST or None, files=request.FILES or None)

    if form.is_valid():
        location_redirect = form.save()
        return redirect(**location_redirect)

    context = {
        'form': form,
    }

    return render(request, 'users_new.html', context)

@login_required
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