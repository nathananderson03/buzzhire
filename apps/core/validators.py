from django.core import validators

mobile_validator = validators.RegexValidator(r'^07[0-9 ]{9,11}$',
                           'Please enter a valid UK mobile phone number in '
                           'the form 07xxx xxx xxx')
