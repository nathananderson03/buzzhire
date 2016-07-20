from django import forms
from .models import BookingFeedback
from .widgets import RatingWidget
from django.forms.widgets import HiddenInput, Textarea
from crispy_forms.helper import FormHelper


class BookingFeedbackForm(forms.ModelForm):
    """Form used as part of a formset in the leave feedback form.
    
    The form should have an unsaved BookingFeedback instance passed to it
    in the initial data keyed with 'instance'. This is because,
    as part of a formset, it's easier to pass unique values as initial data,
    rather than via the form constructor.
    
    In order to help the view do this, we provide a get_initial() classmethod,
    that should be passed the feedback instance.
    """
    def __init__(self, *args, **kwargs):
        super(BookingFeedbackForm, self).__init__(*args, **kwargs)

        # Part of a formset, so we don't want to show the form tag
        self.helper = FormHelper(self)
        self.helper.form_tag = False

    @classmethod
    def get_initial(cls, feedback):
        """Returns the initial values for the form,
        for the supplied BookingFeedback instance.
        """
        return {'instance': feedback,
                'booking': feedback.booking,
                'author_type': feedback.author_type}

    def feedback_target(self):
        "Returns the client / freelancer that the feedback is for."
        return self.initial['instance'].get_target()

    def clean(self):
        cleaned_data = super(BookingFeedbackForm, self).clean()

        # Put the BookingFeedback instance in the cleaned data

        # Prepare an instance to save
        cleaned_data['instance'] = self.initial['instance']
        cleaned_data['instance'].score = self.cleaned_data['score']
        cleaned_data['instance'].comment = self.cleaned_data['comment']

        return cleaned_data

    def save(self):
        "Create the BookingFeedback in the database."
        self.cleaned_data['instance'].save()

    class Meta:
        model = BookingFeedback
        widgets = {
            'score': RatingWidget,
            'author_type': HiddenInput,
            'booking': HiddenInput,
            'comment': Textarea(attrs={'rows': 3})
        }
        fields = ('score', 'author_type', 'booking', 'comment')
