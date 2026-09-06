import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="ชื่อหมวดหมู่")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="วันที่สร้าง")),
            ],
            options={
                "verbose_name": "หมวดหมู่",
                "verbose_name_plural": "หมวดหมู่",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Expense",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(verbose_name="วันที่")),
                ("title", models.CharField(max_length=200, verbose_name="รายการ")),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="จำนวนเงิน")),
                ("note", models.TextField(blank=True, verbose_name="หมายเหตุ")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="สร้างเมื่อ")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="แก้ไขล่าสุด")),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="expenses",
                        to="expenses.category",
                        verbose_name="หมวดหมู่",
                    ),
                ),
            ],
            options={
                "verbose_name": "ค่าใช้จ่าย",
                "verbose_name_plural": "ค่าใช้จ่าย",
                "ordering": ["-date", "-created_at"],
            },
        ),
    ]
