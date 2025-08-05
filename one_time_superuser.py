import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "water_delivery.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Choose a unique identifier for checking if the user already exists
if not User.objects.filter(id_number="0000000000000").exists():
    User.objects.create_superuser(
        username="admin",  # <-- FIXED: Required field!
        id_number="0000000000000",
        email="admin@example.com",
        password="adminpassword123",
        first_name="Admin",
        last_name="User",
        phone_number="0123456789",
        address="Admin Office",
        is_staff=True,
        is_superuser=True
    )
    print("✅ Superuser created")
else:
    print("ℹ️ Superuser already exists")
