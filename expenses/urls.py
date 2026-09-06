from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    # Expense
    path("expenses/", views.expense_list, name="expense_list"),
    path("expenses/add/", views.expense_create, name="expense_create"),
    path("expenses/<int:pk>/edit/", views.expense_update, name="expense_update"),
    path("expenses/<int:pk>/delete/", views.expense_delete, name="expense_delete"),
    # Income
    path("incomes/", views.income_list, name="income_list"),
    path("incomes/add/", views.income_create, name="income_create"),
    path("incomes/<int:pk>/edit/", views.income_update, name="income_update"),
    path("incomes/<int:pk>/delete/", views.income_delete, name="income_delete"),
    # Category
    path("categories/", views.category_list, name="category_list"),
    path("categories/add/", views.category_create, name="category_create"),
    path("categories/<int:pk>/edit/", views.category_update, name="category_update"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
    # Summary
    path("summary/", views.monthly_summary, name="monthly_summary"),
]
