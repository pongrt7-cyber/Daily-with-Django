import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def messages_to_json(messages):
    """แปลง Django messages framework queryset ให้เป็น JSON string
    สำหรับฝัง <script type="application/json"> แล้วอ่านด้วย JS (SweetAlert2)."""
    data = [{"message": str(m), "tags": m.tags} for m in messages]
    return mark_safe(json.dumps(data))
