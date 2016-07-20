from djmoney.forms.widgets import MoneyWidget
from django.forms.widgets import TextInput, RadioSelect, RadioFieldRenderer


class Bootstrap3SterlingMoneyWidget(MoneyWidget):
    """Bootstrap 3 style money widget for GBP.
    Usage:
    
        in __init__ method:
        
        amount, currency = self.fields['my_field_name'].fields
        self.fields['my_field_name'].widget = Bootstrap3SterlingMoneyWidget(
           amount_widget=amount.widget, currency_widget=widgets.HiddenInput)
    """
    def format_output(self, rendered_widgets):
        return ("""<div class="input-group">
            <span class="input-group-addon">&pound;</span>
            %s%s
            </div>""" % tuple(rendered_widgets))


class Bootstrap3TextInput(TextInput):
    """Bootstrap 3 style text input.
    Usage:
    
        
    """
    def __init__(self, *args, **kwargs):
        self.addon_before = kwargs.pop('addon_before', '')
        self.addon_after = kwargs.pop('addon_after', '')
        super(Bootstrap3TextInput, self).__init__(*args, **kwargs)

    def render(self, *args, **kwargs):
        output = ''
        if self.addon_before:
            output += '<span class="input-group-addon">%s</span>' % self.addon_before
        output += super(Bootstrap3TextInput, self).render(*args, **kwargs)
        if self.addon_after:
            output += '<span class="input-group-addon">%s</span>' % self.addon_after
        return '<div class="input-group">%s</div>' % output


class ChoiceAttrsRadioSelect(RadioSelect):
    """Widget that allows you to specify custom attrs for each 
    individual choice.  Needs to be used in tandem with a renderer that
    process the choice attrs dictionary using the flatatt_for_choice filter.
    
    See templates/bootstrap3/layout/radioselect.html for an example of
    a template.
    
    Usage:
    
        widget = ChoiceAttrsRadioSelect(choice_attrs={
            1: {'foo': 'bar'},
            2: {'fizz': 'buzz'},
        })
    """
    def __init__(self, *args, **kwargs):
        self.choice_attrs = kwargs.pop('choice_attrs', [])
        super(ChoiceAttrsRadioSelect, self).__init__(*args, **kwargs)
