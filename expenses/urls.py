from django.urls import path
from . import views
from . import budget_views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('budgets/', budget_views.budget_list, name='budget_list'),
    path('settings/', views.settings_view, name='settings'),
    path('edit/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('export/', views.export_expenses, name='export_expenses'),
]
