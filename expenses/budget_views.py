from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from .models import Budget, Category, Expense, UserSettings
from .forms import BudgetForm
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime

def budget_list(request):
    current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            # Handle unique constraint manually if needed or let form handle it (it might error if duplicate)
            try:
                form.save()
            except:
                # Simple error handling for duplicate budget
                pass
            return redirect('budget_list')
    else:
        form = BudgetForm(initial={'month': current_month})

    budgets = Budget.objects.filter(month__year=current_month.year, month__month=current_month.month)
    
    # Calculate progress for each budget
    budget_data = []
    for budget in budgets:
        spent = Expense.objects.filter(
            category=budget.category,
            date__year=current_month.year,
            date__month=current_month.month
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        
        percent = (spent / budget.amount) * 100 if budget.amount > 0 else 0
        
        budget_data.append({
            'category': budget.category.name,
            'limit': budget.amount,
            'spent': spent,
            'percent': min(percent, 100),
            'is_over': spent > budget.amount
        })

    settings = UserSettings.get_settings()
    currency = settings.currency_symbol

    context = {
        'form': form,
        'budget_data': budget_data,
        'current_month': current_month,
        'currency': currency,
    }
    return render(request, 'expenses/budget_list.html', context)
