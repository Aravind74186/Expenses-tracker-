from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Expense(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"

class Budget(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(help_text="First day of the month for this budget")
    
    class Meta:
        unique_together = ['category', 'month']

    def __str__(self):
        return f"{self.category} - {self.amount} ({self.month.strftime('%Y-%m')})"

class UserSettings(models.Model):
    currency_symbol = models.CharField(max_length=10, default='$')
    currency_code = models.CharField(max_length=10, default='USD')

    def __str__(self):
        return f"Settings ({self.currency_code})"

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
