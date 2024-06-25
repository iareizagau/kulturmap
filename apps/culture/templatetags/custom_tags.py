from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def set_previous_date(context, current_date):
    previous_date = context.get('previous_date', None)
    context['previous_date'] = current_date
    return previous_date != current_date
