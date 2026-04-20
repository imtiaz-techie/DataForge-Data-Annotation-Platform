from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import CustomUser
from .forms import RegisterForm, LoginForm, ProfileForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created! Welcome to DataForge.')
        return redirect('dashboard:home')
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('accounts:profile')

    # Compute stats
    from apps.annotations.models import Annotation
    total_annotated = Annotation.objects.filter(annotator=request.user).count()
    verified = Annotation.objects.filter(annotator=request.user, verified=True).count()

    context = {
        'form': form,
        'total_annotated': total_annotated,
        'verified': verified,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def user_list_view(request):
    """Admin-only: list all users."""
    if not request.user.is_admin():
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_list.html', {'users': users})


@login_required
@require_POST
def toggle_user_status(request, user_id):
    if not request.user.is_admin():
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    try:
        user = CustomUser.objects.get(pk=user_id)
        if user != request.user:
            user.is_active = not user.is_active
            user.save()
            status = 'activated' if user.is_active else 'deactivated'
            messages.success(request, f'User {user.username} {status}.')
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')
    return redirect('accounts:user_list')
