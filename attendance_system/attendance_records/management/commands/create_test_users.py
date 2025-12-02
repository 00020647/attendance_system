from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


class Command(BaseCommand):
    help = 'Create test users (student, tutor, admin) and groups'

    def handle(self, *args, **options):
        # Create groups if they don't exist
        student_group, _ = Group.objects.get_or_create(name='Students')
        tutor_group, _ = Group.objects.get_or_create(name='Tutors')

        self.stdout.write(self.style.SUCCESS('✓ Groups created'))

        # Test accounts
        test_accounts = [
            {'username': 'student', 'password': 'password123', 'group': 'Students'},
            {'username': 'tutor', 'password': 'password123', 'group': 'Tutors'},
            {'username': 'admin', 'password': 'password123', 'is_staff': True, 'is_superuser': True},
        ]

        for account in test_accounts:
            username = account['username']
            password = account['password']
            
            # Create user if doesn't exist
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'is_staff': account.get('is_staff', False),
                    'is_superuser': account.get('is_superuser', False),
                }
            )

            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✓ User "{username}" created with password "{password}"'))
            else:
                # Reset password for existing user
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.WARNING(f'⚠ User "{username}" already exists, password reset to "{password}"'))

            # Add to group (except admin)
            if 'group' in account:
                group_name = account['group']
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
                self.stdout.write(self.style.SUCCESS(f'  → Added to group "{group_name}"'))

        self.stdout.write(self.style.SUCCESS('\n✓ All test accounts created successfully!'))
