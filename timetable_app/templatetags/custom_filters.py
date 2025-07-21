from django import template

register = template.Library()

# Define the weekday order
DAY_ORDER = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6,
}

@register.filter
def sort_by_day(day_list):
    """
    Sort a list of weekday strings (e.g., ['Wednesday', 'Monday', 'Friday']) 
    into proper chronological order from Monday to Sunday.
    """
    if isinstance(day_list, list):
        # Filter out any None or invalid items
        valid_days = [day for day in day_list if isinstance(day, str)]
        return sorted(valid_days, key=lambda day: DAY_ORDER.get(day, 99))
    return day_list

@register.filter
def dict_get(d, key):
    """
    Access dictionary value by key.
    Usage: {{ my_dict|dict_get:key }}
    """
    if isinstance(d, dict):
        return d.get(key, 'N/A')
    return 'N/A'

@register.filter
def get_item(dictionary, key):
    """
    Access dictionary value by key (alternate name).
    Usage: {{ my_dict|get_item:key }}
    """
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

@register.filter
def split(value, key):
    """
    Split a string value by a delimiter.
    Usage: {{ "a,b,c"|split:"," }}
    """
    if not isinstance(value, str):
        return value
    return value.split(key)

@register.filter
def to_int(value):
    """
    Convert value to integer.
    Usage: {{ value|to_int }}
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


