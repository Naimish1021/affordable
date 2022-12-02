from django import template

register = template.Library()

def replace_text(value,args):
    return value.replace(args,'')
register.filter("replace",replace_text)