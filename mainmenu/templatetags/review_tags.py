from django import template
from django.db.models import Avg

register = template.Library()

@register.filter
def avg_rating(reviews):
    if not reviews:
        return 0
    return round(reviews.aggregate(Avg('rating'))['rating__avg'] or 0, 1) 