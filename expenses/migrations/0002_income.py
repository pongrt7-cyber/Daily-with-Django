from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Income",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(verbose_name="วันที่")),
                ("title", models.CharField(max_length=200, verbose_name="รายการ")),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10, verbose_name="จำนวนเงิน")),
                ("note", models.TextField(blank=True, verbose_name="หมายเหตุ")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="สร้างเมื่อ")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="แก้ไขล่าสุด")),
            ],
            options={
                "verbose_name": "รายรับ",
                "verbose_name_plural": "รายรับ",
                "ordering": ["-date", "-created_at"],
            },
        ),
    ]
