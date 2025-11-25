from django import forms
from .models import Expense, Category, Budget

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'category', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month']
        widgets = {
            'month': forms.DateInput(attrs={'type': 'month'}),
        }

from .models import UserSettings

class SettingsForm(forms.ModelForm):
    CURRENCY_CHOICES = [
        ('USD', 'USD ($)'),
        ('EUR', 'EUR (€)'),
        ('GBP', 'GBP (£)'),
        ('INR', 'INR (₹)'),
        ('JPY', 'JPY (¥)'),
        ('CNY', 'CNY (¥)'),
        ('AUD', 'AUD ($)'),
        ('CAD', 'CAD ($)'),
    ]
    
    currency_code = forms.ChoiceField(choices=CURRENCY_CHOICES)

    class Meta:
        model = UserSettings
        fields = ['currency_code']

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Map code to symbol
        symbols = {
            'USD': '$', 'EUR': '€', 'GBP': '£', 'INR': '₹', 
            'JPY': '¥', 'CNY': '¥', 'AUD': '$', 'CAD': '$'
        }
        instance.currency_symbol = symbols.get(instance.currency_code, '$')
        if commit:
            instance.save()
        return instance

