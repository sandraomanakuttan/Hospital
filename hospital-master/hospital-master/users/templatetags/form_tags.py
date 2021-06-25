from django import template

register = template.Library()


def get_label(a_dict, key):
    return getattr(a_dict.get(key), 'label', 'No label')

def display_or_None(a,b):
    if len(a)>0:
        return a
    else:
        return b

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


register.filter("get_label", get_label)
register.filter("display_or_None", display_or_None)
register.filter('get_item',get_item)