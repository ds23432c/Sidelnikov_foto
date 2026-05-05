from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import OrderRequest, ServiceOffer
from .forms import OrderRequestForm, ServiceOfferForm
from apps.accounts.models import User
from apps.notifications.models import Notification


@login_required
def create_order(request, username):
    creator = get_object_or_404(User, username=username, role='creator')
    if request.method == 'POST':
        form = OrderRequestForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.user
            order.creator = creator
            order.save()
            Notification.objects.create(
                recipient=creator,
                sender=request.user,
                type='order',
                text=f'Новая заявка от {request.user.username}: {order.project_type}'
            )
            messages.success(request, 'Заявка отправлена!')
            return redirect('profile', username=username)
    else:
        form = OrderRequestForm()
    return render(request, 'orders/create_order.html', {'form': form, 'creator': creator})


@login_required
def order_list(request):
    orders_in = OrderRequest.objects.filter(creator=request.user).select_related('client')
    orders_out = OrderRequest.objects.filter(client=request.user).select_related('creator')
    return render(request, 'orders/order_list.html', {
        'orders_in': orders_in,
        'orders_out': orders_out,
    })


@login_required
def update_status(request, pk):
    order = get_object_or_404(OrderRequest, pk=pk, creator=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(OrderRequest.STATUS_CHOICES):
            order.status = new_status
            order.save()
            Notification.objects.create(
                recipient=order.client,
                sender=request.user,
                type='order',
                text=f'Статус вашей заявки изменён на «{order.get_status_display()}»'
            )
    return redirect('order_list')


@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceOfferForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.creator = request.user
            service.save()
            messages.success(request, 'Услуга добавлена')
            return redirect('cabinet')
    else:
        form = ServiceOfferForm()
    return render(request, 'orders/service_form.html', {'form': form})


@login_required
def service_delete(request, pk):
    service = get_object_or_404(ServiceOffer, pk=pk, creator=request.user)
    if request.method == 'POST':
        service.delete()
    return redirect('cabinet')
