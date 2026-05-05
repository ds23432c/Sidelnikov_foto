from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Ensure the default superuser exists'

    def handle(self, *args, **options):
        user_model = get_user_model()
        username = settings.DJANGO_SUPERUSER_USERNAME
        email = settings.DJANGO_SUPERUSER_EMAIL
        password = settings.DJANGO_SUPERUSER_PASSWORD

        user, created = user_model.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_superuser': True,
            },
        )

        if created:
            user.set_password(password)
            user.save(update_fields=['password'])
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created.'))
            return

        updated_fields = []
        if email and user.email != email:
            user.email = email
            updated_fields.append('email')
        if not user.is_staff:
            user.is_staff = True
            updated_fields.append('is_staff')
        if not user.is_superuser:
            user.is_superuser = True
            updated_fields.append('is_superuser')

        if updated_fields:
            user.save(update_fields=updated_fields)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" updated.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" already exists.'))
