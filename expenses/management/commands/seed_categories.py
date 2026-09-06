from django.core.management.base import BaseCommand

from expenses.models import Category

DEFAULT_CATEGORIES = [
    "อาหาร",
    "เดินทาง",
    "ของใช้ประจำวัน",
    "ที่พัก",
    "ค่าน้ำค่าไฟ",
    "สุขภาพ",
    "บันเทิง",
    "การศึกษา",
    "ครอบครัว",
    "อื่น ๆ",
]


class Command(BaseCommand):
    help = "สร้างหมวดหมู่ค่าใช้จ่ายเริ่มต้น (ข้ามหมวดที่มีอยู่แล้ว)"

    def handle(self, *args, **options):
        created_count = 0
        for name in DEFAULT_CATEGORIES:
            _, created = Category.objects.get_or_create(name=name)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"เพิ่มหมวดหมู่: {name}"))
            else:
                self.stdout.write(f"มีอยู่แล้ว: {name}")

        if created_count:
            self.stdout.write(self.style.SUCCESS(f"เสร็จสิ้น: เพิ่มหมวดหมู่ใหม่ {created_count} รายการ"))
        else:
            self.stdout.write("ไม่มีหมวดหมู่ใหม่ที่ต้องเพิ่ม (มีครบอยู่แล้ว)")
