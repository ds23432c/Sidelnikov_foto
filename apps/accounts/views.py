from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import User, Follow
from .forms import RegisterForm, LoginForm, ProfileEditForm
from apps.works.models import Work, Album
from apps.orders.models import ServiceOffer, OrderRequest
from apps.notifications.models import Notification


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.creator_type = form.cleaned_data.get('creator_type') or None
            user.save()
            login(request, user)
            messages.success(request, 'Добро пожаловать на Folio!')
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get('next', '/'))
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def profile_view(request, username):
    creator = get_object_or_404(User, username=username)
    works = Work.objects.filter(creator=creator, is_published=True).order_by('-created_at')
    albums = Album.objects.filter(creator=creator)
    services = ServiceOffer.objects.filter(creator=creator)
    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, following=creator).exists()
    total_likes = sum(w.likes_count for w in works)
    return render(request, 'accounts/profile.html', {
        'creator': creator,
        'works': works,
        'albums': albums,
        'services': services,
        'is_following': is_following,
        'total_likes': total_likes,
    })


@login_required
def follow_toggle(request, username):
    target = get_object_or_404(User, username=username)
    if request.user == target:
        return JsonResponse({'error': 'Нельзя подписаться на себя'}, status=400)
    follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
    if not created:
        follow.delete()
        target.followers_count = max(0, target.followers_count - 1)
        target.save()
        following = False
    else:
        target.followers_count += 1
        target.save()
        following = True
        Notification.objects.create(
            recipient=target,
            sender=request.user,
            type='follow',
            text=f'{request.user.username} подписался на вас'
        )
    return JsonResponse({'following': following, 'count': target.followers_count})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён')
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
def my_cabinet(request):
    user = request.user
    works = Work.objects.filter(creator=user).order_by('-created_at')
    orders_in = OrderRequest.objects.filter(creator=user).order_by('-created_at')
    orders_out = OrderRequest.objects.filter(client=user).order_by('-created_at')
    followed_users = Follow.objects.filter(follower=user).select_related('following')
    feed_works = Work.objects.filter(
        creator__in=[f.following for f in followed_users],
        is_published=True
    ).order_by('-created_at')[:20]
    return render(request, 'accounts/cabinet.html', {
        'works': works,
        'orders_in': orders_in,
        'orders_out': orders_out,
        'feed_works': feed_works,
    })
