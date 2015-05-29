# oscm_app/templatetags

from django import template
from django.template.loader import render_to_string

register = template.Library()


def silence_without_field(fn):
    def wrapped(field, attr):
        if not field:
            return ""
        return fn(field, attr)
    return wrapped


def _process_field_attributes(field, attr, process):
    # split attribute name and value from 'attr:value' string
    params = attr.split(':', 1)
    attribute = params[0]
    value = params[1] if len(params) == 2 else ''

    # decorate field.as_widget method with updated attributes
    old_as_widget = field.as_widget

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        attrs = attrs or {}
        process(widget or self.field.widget, attrs, attribute, value)
        return old_as_widget(widget, attrs, only_initial)

    bound_method = type(old_as_widget)
    field.as_widget = bound_method(as_widget, field)
    return field


@register.filter
def bootstrapform(form):
    return render_to_string('bootstrapform.html', {'form': form})


@register.filter("attr")
@silence_without_field
def set_attr(field, attr):
    def process(widget, attrs, attribute, value):
        attrs[attribute] = value
    return _process_field_attributes(field, attr, process)


@register.filter("append_attr")
@silence_without_field
def append_attr(field, attr):
    def process(widget, attrs, attribute, value):
        if attrs.get(attribute):
            attrs[attribute] += ' ' + value
        elif widget.attrs.get(attribute):
            attrs[attribute] = widget.attrs[attribute] + ' ' + value
        else:
            attrs[attribute] = value
    return _process_field_attributes(field, attr, process)


@register.filter
def bootstrapform_field_id(field):
    try:
        if (hasattr(field, 'field')) and (
                hasattr(field.field, 'widget')) and (field.field.widget):
            widget = field.field.widget
            widget_type = field.field.__class__.__name__.lower()
            if widget_type == 'BooleanField'.lower():
                css_class = "checkbox"
                append_attr(field, 'class:' + css_class)
            else:
                css_class = "form-control"
                append_attr(field, 'class:' + css_class)
    except AttributeError:
        widget = field.widget
    return widget.attrs.get(id, field.auto_id)
