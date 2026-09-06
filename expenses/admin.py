from django.contrib import admin

from .models import Category, Expense, Income


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("date", "title", "amount", "category", "updated_at")
    list_filter = ("category", "date")
    search_fields = ("title", "note")
    date_hierarchy = "date"
    ordering = ("-date",)
    autocomplete_fields = ("category",)


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ("date", "title", "amount", "updated_at")
    list_filter = ("date",)
    search_fields = ("title", "note")
    date_hierarchy = "date"
    ordering = ("-date",)
