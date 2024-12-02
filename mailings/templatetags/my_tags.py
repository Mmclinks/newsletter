from django import template

register = template.Library()


@register.filter()
def media_filter(path):
    """
    Фильтр для медиаданных
    """
    if path:
        return f"/media/{path}"
    return "#"


@register.filter(name="add_class")
def add_class(field, css_class):
    """
    Фильтр для стилизации форм
    """
    return field.as_widget(attrs={"class": css_class})


@register.filter
def is_in_group(user, group_name):
    """
    Проверяет, состоит ли пользователь в указанной группе.
    """
    return user.groups.filter(name=group_name).exists()
