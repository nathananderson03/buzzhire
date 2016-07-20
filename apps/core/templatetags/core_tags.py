from django import template
from django.template.loader import render_to_string, select_template
from django.conf import settings
from copy import copy
from crispy_forms.templatetags.crispy_forms_filters import flatatt_filter
from apps.core.utils import template_names_from_polymorphic_model
import datetime


register = template.Library()

@register.filter
def get_field_title(object, field_name):
    """Loads the practioner model based on its pk.
    
    Usage:
    
        {{ object|get_field_title:'my_field_name' }}
    """
    return object._meta.get_field(field_name).verbose_name


@register.filter
def get_field_value(object, field_name):
    """Outputs the value of an object's field.
    Equivalent to {{ object.field_name }}.
    
    Usage:
    
        {{ object|get_field_value:'my_field_name' }}
    """
    return getattr(object, field_name)


@register.filter
def instances_and_widgets(bound_field):
    """Returns a list of two-tuples of instances and widgets, designed to
    be used with ModelMultipleChoiceField and CheckboxSelectMultiple widgets.
    
    Allows templates to loop over a multiple checkbox field and display the
    related model instance, such as for a table with checkboxes.
      
    Usage:
        {% for instance, widget in form.my_field_name|instances_and_widgets %}
            <p>{{ instance }}: {{ widget }}</p> 
        {% endfor %}
    """
    instance_widgets = []
    index = 0
    for instance in bound_field.field.queryset.all():
         widget = copy(bound_field[index])
         # Hide the choice label so it just renders as a checkbox
         widget.choice_label = ''
         instance_widgets.append((instance, widget))
         index += 1
    return instance_widgets


@register.filter
def get_non_page_options(request):
    """Returns a urlencoded version of the GET options passed to the request,
    with the paginator page option removed.
    
    Used by templates/includes/paginator.html."""
    querydict = request.GET.copy()
    querydict.pop('page', None)
    return querydict.urlencode


@register.filter
def startswith(test_string, start_string):
    """Returns whether comparison string starts with the original string.
    Usage:
    
      {% if test_string|startswith:start_string %}
          <p>'{{ test_string }}' starts with '{{ start_string }}'!
      {% endif %}
    """
    # Note we cast start_string as a string, in case it's been
    # passed here using reverse_lazy
    return test_string.startswith(str(start_string))


@register.simple_tag
def base_url():
    """Returns the base url.
    
    Usage:
    
        {% base_url %}
    """
    return settings.BASE_URL


@register.filter
def flatatt_for_choice(widget, choice_value):
    """Outputs the attributes for the supplied widget and choice.  Designed to
    be used with apps.core.widgets.ChoiceAttrsRadioSelect.
    
    Usage:
        {% for choice in field.field.choices %}
            <input type="radio"
                {{ field.field.widget|flatatt_for_choice:choice.0 }}>
                {{ choice.1|unlocalize }}
        {% endfor %}
    """
    choice_attrs = copy(widget.attrs)
    try:
        choice_attrs.update(widget.choice_attrs[choice_value])
    except (AttributeError, KeyError):
        pass
    return flatatt_filter(choice_attrs)


@register.filter
def model_opts(instance):
    "Returns the _meta attribute from the supplied model."
    return instance._meta


@register.simple_tag(takes_context=True)
def summary(context, instance):
    """Outputs a summary of the supplied model instance.
    Usage:
    
        {% summary object %}
    """
    template_names = template_names_from_polymorphic_model(
                                instance.__class__, '_summary',
                                'includes')
    return render_to_string(template_names, {'object': instance,
                                             'request': context['request']})


@register.simple_tag
def summary_for_email(instance, audience):
    """Outputs a summary of the supplied model instance, suitable for email,
    for the appropriate audience ('freelancer', 'client', 'admin').
    
    Usage:
    
        {% summary_for_email driver_job_request 'client' %}
        
        This will pass the supplied driver job request to
        'driver/email/includes/driverjobrequest_client_summary.html', falling
        back to 'job/email/includes/jobrequest_client_summary.html'.
    """

    template_names = template_names_from_polymorphic_model(instance.__class__,
                                            suffix='_%s_summary' % audience,
                                            subdirectory='email/includes')
    # Pass the available base template to the context.  This allows
    # templates to extend the base template specific to the model type,
    # without us needing to create specific templates for each suffix
    # for that type.  For example, we can create a specific base template
    # for DriverJobRequest without needing to have a specific DriverJobRequest
    # client template to extend it.
    base_template = select_template(template_names_from_polymorphic_model(
                                    instance.__class__,
                                    suffix='_base_summary',
                                    subdirectory='email/includes')).name
    return render_to_string(template_names, {'object': instance,
                                             'base_template': base_template})


@register.filter
def istoday(date):
    """Returns whether or not the supplied date is today.
    
    Usage:
    
        {% if object.date|istoday %}
            {# Do something #}
        {% endif %}
    """
    return date == datetime.date.today()