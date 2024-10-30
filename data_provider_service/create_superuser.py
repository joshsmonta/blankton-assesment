import os
from django.contrib.auth.models import User
from django.core.management import execute_from_command_line

# Retrieve username, password, and email from environment variables
admin_username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
admin_password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin')
admin_email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')

# Check if the superuser already exists
if not User.objects.filter(username=admin_username).exists():
    User.objects.create_superuser(
        username=admin_username,
        password=admin_password,
        email=admin_email
    )
    print("Superuser created successfully.")
else:
    print("Superuser already exists.")
