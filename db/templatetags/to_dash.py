from django import template
from django.template.defaultfilters import slugify 
register = template.Library()

def to_dash(value):
    return slugify(value)
register.filter("to_dash",to_dash)