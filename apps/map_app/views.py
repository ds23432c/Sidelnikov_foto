from django.shortcuts import render
from django.http import JsonResponse
from apps.accounts.models import User


def map_view(request):
    return render(request, 'map_app/map.html')


def creators_json(request):
    creator_type = request.GET.get('type')
    creators = User.objects.filter(role='creator').exclude(latitude=None).exclude(longitude=None)
    if creator_type:
        creators = creators.filter(creator_type=creator_type)

    data = []
    for u in creators:
        data.append({
            'id': u.pk,
            'username': u.username,
            'name': u.get_full_name() or u.username,
            'creator_type': u.get_creator_type_display_ru(),
            'city': u.city,
            'avatar': u.get_avatar() or '',
            'specialization': u.specialization,
            'lat': u.latitude,
            'lng': u.longitude,
            'url': f'/accounts/u/{u.username}/',
        })
    return JsonResponse({'creators': data})
