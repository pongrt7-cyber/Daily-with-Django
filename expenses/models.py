from django.db import models


class Category(models.Model):
    """หมวดหมู่ของค่าใช้จ่าย เช่น อาหาร, เดินทาง, ที่พัก"""

    name = models.CharField("ชื่อหมวดหมู่", max_length=100, unique=True)
    created_at = models.DateTimeField("วันที่สร้าง", auto_now_add=True)

    class Meta:
        verbose_name = "หมวดหมู่"
        verbose_name_plural = "หมวดหมู่"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Expense(models.Model):
    """รายการค่าใช้จ่าย"""

    date = models.DateField("วันที่")
    title = models.CharField("รายการ", max_length=200)
    amount = models.DecimalField("จำนวนเงิน", max_digits=10, decimal_places=2)
    note = models.TextField("หมายเหตุ", blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="expenses",
        verbose_name="หมวดหมู่",
    )
    created_at = models.DateTimeField("สร้างเมื่อ", auto_now_add=True)
    updated_at = models.DateTimeField("แก้ไขล่าสุด", auto_now=True)

    class Meta:
        verbose_name = "ค่าใช้จ่าย"
        verbose_name_plural = "ค่าใช้จ่าย"
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.title} ({self.amount})"


class Income(models.Model):
    """รายการรายรับ"""

    date = models.DateField("วันที่")
    title = models.CharField("รายการ", max_length=200)
    amount = models.DecimalField("จำนวนเงิน", max_digits=10, decimal_places=2)
    note = models.TextField("หมายเหตุ", blank=True)
    created_at = models.DateTimeField("สร้างเมื่อ", auto_now_add=True)
    updated_at = models.DateTimeField("แก้ไขล่าสุด", auto_now=True)

    class Meta:
        verbose_name = "รายรับ"
        verbose_name_plural = "รายรับ"
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.title} ({self.amount})"
