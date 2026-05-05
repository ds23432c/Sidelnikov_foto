from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.db.models import Count, Sum
from apps.accounts.models import User
from apps.works.models import Work, Comment, Like
from apps.orders.models import OrderRequest
from apps.messages_app.models import Message
from apps.notifications.models import Notification


def is_admin(user):
    return user.is_authenticated and (user.role == 'admin' or user.is_staff)


@login_required
@user_passes_test(is_admin, login_url='/')
def dashboard(request):
    stats = {
        'users': User.objects.count(),
        'creators': User.objects.filter(role='creator').count(),
        'works': Work.objects.count(),
        'published': Work.objects.filter(is_published=True).count(),
        'likes': Like.objects.count(),
        'orders': OrderRequest.objects.count(),
        'messages': Message.objects.count(),
        'comments': Comment.objects.count(),
    }
    top_creators = User.objects.filter(role='creator').order_by('-works_count', '-followers_count')[:10]

    from django.utils import timezone
    from datetime import timedelta
    days_labels = []
    days_works = []
    for i in range(7, 0, -1):
        day = timezone.now().date() - timedelta(days=i-1)
        days_labels.append(day.strftime('%d.%m'))
        days_works.append(Work.objects.filter(created_at__date=day).count())

    return render(request, 'admin_panel/dashboard.html', {
        'stats': stats,
        'top_creators': top_creators,
        'days_labels': days_labels,
        'days_works': days_works,
    })


@login_required
@user_passes_test(is_admin, login_url='/')
def users_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_panel/users.html', {'users': users})


@login_required
@user_passes_test(is_admin, login_url='/')
def toggle_user_active(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = not user.is_active
    user.save()
    return JsonResponse({'is_active': user.is_active})


@login_required
@user_passes_test(is_admin, login_url='/')
def toggle_user_verified(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_verified = not user.is_verified
    user.save()
    return JsonResponse({'is_verified': user.is_verified})


@login_required
@user_passes_test(is_admin, login_url='/')
def works_moderation(request):
    works = Work.objects.select_related('creator', 'category').order_by('-created_at')
    return render(request, 'admin_panel/works.html', {'works': works})


@login_required
@user_passes_test(is_admin, login_url='/')
def toggle_work_published(request, pk):
    work = get_object_or_404(Work, pk=pk)
    work.is_published = not work.is_published
    work.save()
    return JsonResponse({'is_published': work.is_published})


@login_required
@user_passes_test(is_admin, login_url='/')
def comments_moderation(request):
    comments = Comment.objects.select_related('user', 'work').order_by('-created_at')
    return render(request, 'admin_panel/comments.html', {'comments': comments})


@login_required
@user_passes_test(is_admin, login_url='/')
def toggle_comment_approved(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.is_approved = not comment.is_approved
    comment.save()
    return JsonResponse({'is_approved': comment.is_approved})
