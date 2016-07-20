# https://github.com/kartik-v/bootstrap-star-rating
from django.forms import widgets


class RatingWidget(widgets.NumberInput):
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = kwargs.get('attrs', {})
        kwargs['attrs'].update({
            'min': '0',
            'max': '5',
            'step': '1',
            'class': 'rating-widget',
        })
        super(RatingWidget, self).__init__(*args, **kwargs)

    class Media:
        css = {
            'all': ('bootstrap-star-rating/css/star-rating.min.css',)
        }
        js = ('bootstrap-star-rating/js/star-rating.min.js',)
