from django import template

register = template.Library()

@register.filter(name='str')
def toStr(value):
    return str(value)
    
