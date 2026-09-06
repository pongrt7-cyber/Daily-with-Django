from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import CategoryForm, ExpenseFilterForm, ExpenseForm, IncomeForm
from .models import Category, Expense, Income

THAI_MONTHS = [
    "", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
    "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม",
]


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
@login_required
def dashboard(request):
    today = timezone.localdate()

    expenses_this_month = Expense.objects.filter(
        date__year=today.year, date__month=today.month
    )
    incomes_this_month = Income.objects.filter(
        date__year=today.year, date__month=today.month
    )

    total_expense = expenses_this_month.aggregate(total=Sum("amount"))["total"] or 0
    total_income = incomes_this_month.aggregate(total=Sum("amount"))["total"] or 0
    balance = total_income - total_expense

    total_expense_all = Expense.objects.aggregate(total=Sum("amount"))["total"] or 0
    total_income_all = Income.objects.aggregate(total=Sum("amount"))["total"] or 0
    balance_all = total_income_all - total_expense_all

    expense_by_category = (
        expenses_this_month.values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )

    recent_expenses = Expense.objects.select_related("category").order_by("-date", "-created_at")[:5]
    recent_incomes = Income.objects.order_by("-date", "-created_at")[:5]

    context = {
        "today": today,
        "month_label": THAI_MONTHS[today.month],
        "total_expense": total_expense,
        "total_income": total_income,
        "balance": balance,
        "total_expense_all": total_expense_all,
        "total_income_all": total_income_all,
        "balance_all": balance_all,
        "expense_by_category": expense_by_category,
        "recent_expenses": recent_expenses,
        "recent_incomes": recent_incomes,
    }
    return render(request, "expenses/dashboard.html", context)


# ---------------------------------------------------------------------------
# Expense CRUD
# ---------------------------------------------------------------------------
@login_required
def expense_list(request):
    expenses = Expense.objects.select_related("category").all()
    form = ExpenseFilterForm(request.GET or None)

    if form.is_valid():
        category = form.cleaned_data.get("category")
        date_from = form.cleaned_data.get("date_from")
        date_to = form.cleaned_data.get("date_to")
        q = form.cleaned_data.get("q")

        if category:
            expenses = expenses.filter(category=category)
        if date_from:
            expenses = expenses.filter(date__gte=date_from)
        if date_to:
            expenses = expenses.filter(date__lte=date_to)
        if q:
            expenses = expenses.filter(title__icontains=q)

    total = expenses.aggregate(total=Sum("amount"))["total"] or 0

    context = {
        "expenses": expenses,
        "form": form,
        "total": total,
    }
    return render(request, "expenses/expense_list.html", context)


@login_required
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "บันทึกรายการค่าใช้จ่ายเรียบร้อยแล้ว")
            return redirect("expense_list")
    else:
        form = ExpenseForm(initial={"date": timezone.localdate()})
    return render(request, "expenses/expense_form.html", {"form": form, "title": "เพิ่มค่าใช้จ่าย"})


@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "แก้ไขรายการค่าใช้จ่ายเรียบร้อยแล้ว")
            return redirect("expense_list")
    else:
        form = ExpenseForm(instance=expense)
    return render(request, "expenses/expense_form.html", {"form": form, "title": "แก้ไขค่าใช้จ่าย"})


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        expense.delete()
        messages.success(request, "ลบรายการค่าใช้จ่ายเรียบร้อยแล้ว")
        return redirect("expense_list")
    return render(request, "expenses/confirm_delete.html", {"object": expense, "cancel_url": "expense_list"})


# ---------------------------------------------------------------------------
# Income CRUD
# ---------------------------------------------------------------------------
@login_required
def income_list(request):
    incomes = Income.objects.all()
    total = incomes.aggregate(total=Sum("amount"))["total"] or 0
    return render(request, "expenses/income_list.html", {"incomes": incomes, "total": total})


@login_required
def income_create(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "บันทึกรายการรายรับเรียบร้อยแล้ว")
            return redirect("income_list")
    else:
        form = IncomeForm(initial={"date": timezone.localdate()})
    return render(request, "expenses/income_form.html", {"form": form, "title": "เพิ่มรายรับ"})


@login_required
def income_update(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, "แก้ไขรายการรายรับเรียบร้อยแล้ว")
            return redirect("income_list")
    else:
        form = IncomeForm(instance=income)
    return render(request, "expenses/income_form.html", {"form": form, "title": "แก้ไขรายรับ"})


@login_required
def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == "POST":
        income.delete()
        messages.success(request, "ลบรายการรายรับเรียบร้อยแล้ว")
        return redirect("income_list")
    return render(request, "expenses/confirm_delete.html", {"object": income, "cancel_url": "income_list"})


# ---------------------------------------------------------------------------
# Category CRUD (จัดการหมวดหมู่ค่าใช้จ่าย)
# ---------------------------------------------------------------------------
@login_required
def category_list(request):
    categories = Category.objects.annotate(expense_total=Sum("expenses__amount"))
    return render(request, "expenses/category_list.html", {"categories": categories})


@login_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "เพิ่มหมวดหมู่เรียบร้อยแล้ว")
            return redirect("category_list")
    else:
        form = CategoryForm()
    return render(request, "expenses/category_form.html", {"form": form, "title": "เพิ่มหมวดหมู่"})


@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "แก้ไขหมวดหมู่เรียบร้อยแล้ว")
            return redirect("category_list")
    else:
        form = CategoryForm(instance=category)
    return render(request, "expenses/category_form.html", {"form": form, "title": "แก้ไขหมวดหมู่"})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        if category.expenses.exists():
            messages.error(request, "ไม่สามารถลบหมวดหมู่นี้ได้ เนื่องจากมีรายการค่าใช้จ่ายผูกอยู่")
        else:
            category.delete()
            messages.success(request, "ลบหมวดหมู่เรียบร้อยแล้ว")
        return redirect("category_list")
    return render(request, "expenses/confirm_delete.html", {"object": category, "cancel_url": "category_list"})


# ---------------------------------------------------------------------------
# สรุปรายเดือน
# ---------------------------------------------------------------------------
@login_required
def monthly_summary(request):
    expense_months = (
        Expense.objects.annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total=Sum("amount"))
    )
    income_months = (
        Income.objects.annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total=Sum("amount"))
    )

    summary = {}
    for row in expense_months:
        key = row["month"]
        summary.setdefault(key, {"expense": 0, "income": 0})
        summary[key]["expense"] = row["total"]
    for row in income_months:
        key = row["month"]
        summary.setdefault(key, {"expense": 0, "income": 0})
        summary[key]["income"] = row["total"]

    rows = []
    for month_date in sorted(summary.keys(), reverse=True):
        data = summary[month_date]
        rows.append(
            {
                "month_date": month_date,
                "month_label": f"{THAI_MONTHS[month_date.month]} {month_date.year + 543}",
                "income": data["income"],
                "expense": data["expense"],
                "balance": data["income"] - data["expense"],
            }
        )

    return render(request, "expenses/monthly_summary.html", {"rows": rows})
