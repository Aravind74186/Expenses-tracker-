from django.shortcuts import render, redirect
from .models import Expense, Category, UserSettings
from .forms import ExpenseForm, SettingsForm
from django.db.models import Sum

def settings_view(request):
    settings = UserSettings.get_settings()
    
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = SettingsForm(instance=settings)
    
    return render(request, 'expenses/settings.html', {'form': form})

def expense_list(request):
    # Get currency settings
    settings = UserSettings.get_settings()
    currency = settings.currency_symbol
    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    expenses = Expense.objects.all().order_by('-date')
    
    from django.core.exceptions import ValidationError
    
    try:
        if start_date:
            expenses = expenses.filter(date__gte=start_date)
        if end_date:
            expenses = expenses.filter(date__lte=end_date)
    except ValidationError:
        # If dates are invalid, ignore them or handle gracefully
        pass

    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum']
    if total_expenses is None:
        total_expenses = 0
    
    # Prepare data for the chart
    category_data = expenses.values('category__name').annotate(total=Sum('amount')).order_by('-total')
    
    # Daily spending trend
    daily_data = expenses.values('date').annotate(daily_total=Sum('amount')).order_by('date')
    
    import json
    from django.core.serializers.json import DjangoJSONEncoder
    
    def default_serializer(obj):
        import decimal
        import datetime
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        raise TypeError
        
    category_data_json = json.dumps(list(category_data), default=default_serializer)
    daily_data_json = json.dumps(list(daily_data), cls=DjangoJSONEncoder, default=default_serializer)

    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()

    context = {
        'expenses': expenses,
        'total_expenses': total_expenses,
        'form': form,
        'category_data': category_data_json,
        'daily_data': daily_data_json,
        'currency': currency,
    }
    return render(request, 'expenses/expense_list.html', context)

def edit_expense(request, pk):
    expense = Expense.objects.get(pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    
    return render(request, 'expenses/expense_edit.html', {'form': form})

def delete_expense(request, pk):
    if request.method == 'POST':
        expense = Expense.objects.get(pk=pk)
        expense.delete()
    return redirect('expense_list')

import csv
from django.http import HttpResponse

def export_expenses(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Category', 'Description', 'Amount'])

    expenses = Expense.objects.all().order_by('-date')
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    from django.core.exceptions import ValidationError
    
    try:
        if start_date:
            expenses = expenses.filter(date__gte=start_date)
        if end_date:
            expenses = expenses.filter(date__lte=end_date)
    except ValidationError:
        pass

    for expense in expenses:
        writer.writerow([expense.date, expense.category.name, expense.description, expense.amount])

    return response
