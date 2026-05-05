from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Work, Category, Tag, Like, Comment, Album, AlbumWork
from .forms import WorkForm, CommentForm
from apps.notifications.models import Notification
import json


def home(request):
    works = Work.objects.filter(is_published=True).select_related('creator', 'category')

    category_slug = request.GET.get('category')
    creator_type = request.GET.get('creator_type')
    city = request.GET.get('city')
    search = request.GET.get('q')

    if category_slug:
        works = works.filter(category__slug=category_slug)
    if creator_type:
        works = works.filter(creator__creator_type=creator_type)
    if city:
        works = works.filter(creator__city__icontains=city)
    if search:
        works = works.filter(Q(title__icontains=search) | Q(tags__name__icontains=search)).distinct()

    paginator = Paginator(works, 24)
    page = request.GET.get('page', 1)
    works_page = paginator.get_page(page)

    from django.utils import timezone
    from datetime import timedelta
    week_ago = timezone.now() - timedelta(days=7)
    top_works = Work.objects.filter(is_published=True, created_at__gte=week_ago).order_by('-likes_count')[:6]

    from apps.accounts.models import User
    new_creators = User.objects.filter(role='creator').order_by('-date_joined')[:6]

    categories = Category.objects.all()
    cities = Work.objects.filter(is_published=True).values_list('creator__city', flat=True).distinct()
    cities = [c for c in cities if c]

    return render(request, 'works/home.html', {
        'works': works_page,
        'top_works': top_works,
        'new_creators': new_creators,
        'categories': categories,
        'cities': sorted(set(cities)),
        'selected_category': category_slug,
        'selected_type': creator_type,
        'selected_city': city,
        'search': search,
    })


def work_detail(request, pk):
    work = get_object_or_404(Work, pk=pk, is_published=True)
    work.views_count += 1
    work.save(update_fields=['views_count'])
    work.creator.views_count += 1
    work.creator.save(update_fields=['views_count'])

    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, work=work).exists()

    comments = work.comments.filter(is_approved=True).select_related('user')
    comment_form = CommentForm()

    similar = Work.objects.filter(creator=work.creator, is_published=True).exclude(pk=pk)[:6]

    return render(request, 'works/work_detail.html', {
        'work': work,
        'is_liked': is_liked,
        'comments': comments,
        'comment_form': comment_form,
        'similar': similar,
    })


@login_required
def like_toggle(request, pk):
    work = get_object_or_404(Work, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, work=work)
    if not created:
        like.delete()
        work.likes_count = max(0, work.likes_count - 1)
        work.save(update_fields=['likes_count'])
        liked = False
    else:
        work.likes_count += 1
        work.save(update_fields=['likes_count'])
        liked = True
        if work.creator != request.user:
            Notification.objects.create(
                recipient=work.creator,
                sender=request.user,
                type='like',
                work=work,
                text=f'{request.user.username} оценил вашу работу «{work.title}»'
            )
    return JsonResponse({'liked': liked, 'count': work.likes_count})


@login_required
def add_comment(request, pk):
    work = get_object_or_404(Work, pk=pk)
    if request.method == 'POST':
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        text = data.get('text', '').strip()
        if text:
            comment = Comment.objects.create(user=request.user, work=work, text=text)
            work.comments_count += 1
            work.save(update_fields=['comments_count'])
            if work.creator != request.user:
                Notification.objects.create(
                    recipient=work.creator,
                    sender=request.user,
                    type='comment',
                    work=work,
                    text=f'{request.user.username} прокомментировал вашу работу «{work.title}»'
                )
            return JsonResponse({
                'ok': True,
                'comment': {
                    'text': comment.text,
                    'user': comment.user.username,
                    'avatar': comment.user.get_avatar() or '',
                    'date': comment.created_at.strftime('%d.%m.%Y %H:%M'),
                }
            })
    return JsonResponse({'ok': False}, status=400)


@login_required
def work_create(request):
    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES)
        if form.is_valid():
            work = form.save(commit=False)
            work.creator = request.user
            work.save()
            form.save_m2m()
            request.user.works_count += 1
            request.user.save(update_fields=['works_count'])
            return redirect('work_detail', pk=work.pk)
    else:
        form = WorkForm()
    return render(request, 'works/work_form.html', {'form': form, 'title': 'Добавить работу'})


@login_required
def work_edit(request, pk):
    work = get_object_or_404(Work, pk=pk, creator=request.user)
    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES, instance=work)
        if form.is_valid():
            form.save()
            return redirect('work_detail', pk=work.pk)
    else:
        form = WorkForm(instance=work)
    return render(request, 'works/work_form.html', {'form': form, 'title': 'Редактировать работу', 'work': work})


@login_required
def work_delete(request, pk):
    work = get_object_or_404(Work, pk=pk, creator=request.user)
    if request.method == 'POST':
        work.delete()
        request.user.works_count = max(0, request.user.works_count - 1)
        request.user.save(update_fields=['works_count'])
        return redirect('cabinet')
    return render(request, 'works/work_confirm_delete.html', {'work': work})
