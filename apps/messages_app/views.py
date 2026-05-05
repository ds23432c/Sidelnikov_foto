from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from .models import Dialog, Message
from apps.accounts.models import User
from apps.notifications.models import Notification
import json


@login_required
def dialog_list(request):
    dialogs = Dialog.objects.filter(participants=request.user).prefetch_related('participants', 'messages')
    dialog_data = []
    for d in dialogs:
        other = d.get_other(request.user)
        last = d.last_message()
        unread = d.unread_count(request.user)
        dialog_data.append({'dialog': d, 'other': other, 'last': last, 'unread': unread})
    dialog_data.sort(key=lambda x: x['dialog'].updated_at, reverse=True)
    return render(request, 'messages_app/dialog_list.html', {'dialog_data': dialog_data})


@login_required
def dialog_detail(request, dialog_id):
    dialog = get_object_or_404(Dialog, pk=dialog_id, participants=request.user)
    other = dialog.get_other(request.user)
    messages_qs = dialog.messages.select_related('sender').all()
    messages_qs.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    return render(request, 'messages_app/dialog_detail.html', {
        'dialog': dialog,
        'other': other,
        'messages': messages_qs,
    })


@login_required
def start_dialog(request, username):
    other = get_object_or_404(User, username=username)
    if other == request.user:
        return redirect('dialog_list')
    dialogs = Dialog.objects.filter(participants=request.user).filter(participants=other)
    if dialogs.exists():
        dialog = dialogs.first()
    else:
        dialog = Dialog.objects.create()
        dialog.participants.add(request.user, other)
    return redirect('dialog_detail', dialog_id=dialog.pk)


@login_required
def send_message(request, dialog_id):
    if request.method == 'POST':
        dialog = get_object_or_404(Dialog, pk=dialog_id, participants=request.user)
        text = request.POST.get('text', '').strip()
        image_url = request.POST.get('image_url', '').strip()
        image = request.FILES.get('image')
        if text or image or image_url:
            msg = Message.objects.create(
                dialog=dialog,
                sender=request.user,
                text=text,
                image_url=image_url,
            )
            if image:
                msg.image = image
                msg.save()
            dialog.save()
            other = dialog.get_other(request.user)
            Notification.objects.create(
                recipient=other,
                sender=request.user,
                type='message',
                text=f'Новое сообщение от {request.user.username}'
            )
            return JsonResponse({
                'ok': True,
                'message': {
                    'text': msg.text,
                    'image': msg.get_image(),
                    'sender': msg.sender.username,
                    'is_mine': True,
                    'time': msg.created_at.strftime('%H:%M'),
                    'avatar': msg.sender.get_avatar() or '',
                }
            })
    return JsonResponse({'ok': False}, status=400)


@login_required
def unread_count_api(request):
    from .models import Message
    count = Message.objects.filter(
        dialog__participants=request.user,
        is_read=False
    ).exclude(sender=request.user).count()
    return JsonResponse({'count': count})
