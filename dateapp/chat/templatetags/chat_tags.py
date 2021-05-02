from django import template


register = template.Library()

@register.filter
def get_participant(obj, username):
    return obj.get_dialog_participant(username)