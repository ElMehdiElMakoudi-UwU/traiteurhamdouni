from django import template

register = template.Library()

@register.filter
def add_class(field, css_class):
    return field.as_widget(attrs={'class': css_class})

@register.filter
def get_item(dictionary, key):
    """
    Custom filter to retrieve a value from a dictionary by its key.
    """
    return dictionary.get(key, '')