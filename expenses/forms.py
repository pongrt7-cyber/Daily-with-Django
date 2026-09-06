from django import forms

from .models import Category, Expense, Income

INPUT_CLASS = (
    "input-dark w-full rounded-lg bg-navy-950/70 border border-white/10 "
    "px-3 py-2.5 text-slate-100 placeholder-slate-500"
)
SELECT_CLASS = (
    "input-dark w-full rounded-lg bg-navy-950/70 border border-white/10 "
    "px-3 py-2.5 text-slate-100"
)
TEXTAREA_CLASS = (
    "input-dark w-full rounded-lg bg-navy-950/70 border border-white/10 "
    "px-3 py-2.5 text-slate-100 placeholder-slate-500"
)


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["date", "title", "amount", "category", "note"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": INPUT_CLASS}),
            "title": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "เช่น ค่าอาหารกลางวัน"}),
            "amount": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01", "min": "0"}),
            "category": forms.Select(attrs={"class": SELECT_CLASS}),
            "note": forms.Textarea(attrs={"class": TEXTAREA_CLASS, "rows": 3, "placeholder": "หมายเหตุ (ถ้ามี)"}),
        }


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ["date", "title", "amount", "note"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": INPUT_CLASS}),
            "title": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "เช่น เงินเดือน"}),
            "amount": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01", "min": "0"}),
            "note": forms.Textarea(attrs={"class": TEXTAREA_CLASS, "rows": 3, "placeholder": "หมายเหตุ (ถ้ามี)"}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "ชื่อหมวดหมู่ใหม่"}),
        }


class ExpenseFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="ทุกหมวดหมู่",
        widget=forms.Select(attrs={"class": SELECT_CLASS}),
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": INPUT_CLASS}),
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": INPUT_CLASS}),
    )
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "ค้นหาชื่อรายการ..."}),
    )
