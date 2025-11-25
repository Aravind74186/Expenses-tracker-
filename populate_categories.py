import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker_core.settings')
django.setup()

from expenses.models import Category

categories = ['Food', 'Transport', 'Utilities', 'Entertainment', 'Health', 'Other']

for name in categories:
    Category.objects.get_or_create(name=name)
    print(f"Created category: {name}")
