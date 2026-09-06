# Daily Expense Tracker with Django

โครงสร้างเริ่มต้นสำหรับระบบบันทึกรายรับรายจ่ายประจำวันด้วย Django

## โครงสร้างหลัก

- `config/` สำหรับตั้งค่าโปรเจกต์
- `expenses/` สำหรับ app หลักของระบบ
- `templates/` สำหรับหน้าเว็บ
- `static/` สำหรับไฟล์ static

## วิธีเริ่มต้น

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_categories
python manage.py createsuperuser
python manage.py runserver
```

## ฟีเจอร์ที่มีในโครงนี้

- เพิ่ม แก้ไข ลบ รายการค่าใช้จ่าย
- เพิ่ม แก้ไข ลบ รายการรายรับ
- Dashboard สรุปยอดรวมและคงเหลือ (ของเดือนนี้ + สะสมทั้งหมด)
- ค้นหา/กรองค่าใช้จ่ายตามหมวดหมู่ ช่วงวันที่ และคำค้น
- ดูสรุปรายเดือนของรายรับและรายจ่าย (แยกตามเดือน)
- จัดการหมวดหมู่ค่าใช้จ่าย (เพิ่ม/แก้ไข/ลบ พร้อมป้องกันการลบหมวดที่มีรายการผูกอยู่)
- จัดการข้อมูลผ่าน Django Admin
- ระบบ Login (ต้องเข้าสู่ระบบก่อนใช้งานทุกหน้า)

## บัญชีผู้ใช้

ไฟล์ `db.sqlite3` ที่แนบมามีข้อมูลตัวอย่างอยู่แล้ว รวมถึงบัญชีผู้ใช้ `admin` (เป็น superuser)
หากจำรหัสผ่านเดิมไม่ได้ ให้รีเซ็ตด้วยคำสั่ง:

```bash
python manage.py changepassword admin
```

หรือสร้างผู้ใช้ใหม่ด้วย `python manage.py createsuperuser`

## URL หลักของระบบ

| หน้า | URL |
| --- | --- |
| Dashboard | `/` |
| รายการค่าใช้จ่าย | `/expenses/` |
| เพิ่มค่าใช้จ่าย | `/expenses/add/` |
| รายการรายรับ | `/incomes/` |
| เพิ่มรายรับ | `/incomes/add/` |
| หมวดหมู่ | `/categories/` |
| สรุปรายเดือน | `/summary/` |
| Django Admin | `/admin/` |
| เข้าสู่ระบบ | `/accounts/login/` |

## โครงสร้างโค้ด

```
config/          ตั้งค่าโปรเจกต์ (settings, urls, wsgi, asgi)
expenses/        แอปหลัก (models, views, forms, admin, urls, migrations)
templates/       เทมเพลตหน้าเว็บ (Bootstrap 5)
static/css/      ไฟล์ CSS เสริม
```

โมเดลหลัก 3 ตัว: `Category`, `Expense` (ผูกกับ Category), `Income` (ไม่มีหมวดหมู่)
ซึ่งตรงกับโครงสร้างเดิมใน `db.sqlite3` ทุกฟิลด์ ทำให้ไม่ต้อง migrate ใหม่ ใช้ข้อมูลเดิมได้ทันที

## แนวทางต่อยอด

- เพิ่มกราฟสรุป (เช่น ใช้ Chart.js) ในหน้า Dashboard หรือสรุปรายเดือน
- เพิ่มระบบงบประมาณ (budget) ต่อหมวดหมู่ พร้อมแจ้งเตือนเมื่อใกล้เกินงบ
- เพิ่ม export ข้อมูลเป็น Excel/CSV
- เพิ่มระบบ multi-user (แยกข้อมูลตามผู้ใช้แต่ละคน โดยเพิ่ม field `user` ในโมเดล)
- ทำ REST API ด้วย Django REST Framework เพื่อต่อกับแอปมือถือในอนาคต
