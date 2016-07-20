from rest_framework import serializers
from apps.core.views import POUND_SIGN
from moneyed import Money
from apps.job import service_from_class

# class ChoiceField(serializers.ChoiceField):
#     """Serializer field that outputs a ChoiceField in the form:
#
#         {
#             'value': 'AB',
#             'text': get_FOO_display(),
#         }
#     """
#
#     def to_representation(self, value):
#         return {
#             'value': value,
#             'text': getattr(self.parent.instance,
#                             'get_%s_display' % self.field_name)(),
#         }
#
#
# class ModelSerializer(serializers.ModelSerializer):
#     serializer_choice_field = MyChoiceField


# class MoneyField(serializers.Field):
#     """Serializer field that outputs a MoneyField in the form:
#
#         {
#             'amount': 7.25,
#             'currency': "GBP",
#         }
#     """
#
#     def to_representation(self, value):
#         return {
#             'amount': value.amount,
#             'currency': str(value.currency),
#             # TODO - make this work for other currencies,
#             # not necessary at the moment
#             # 'display': "%s%s" % (POUND_SIGN, value.amount)
#         }

class MoneyField(serializers.Field):
    """Serializer field that outputs a MoneyField as a decimal (assumes
    GBP currency).
    """
    default_error_messages = {
        'incorrect_format': 'Incorrect format. Expected `###.##`.',
    }

    def to_representation(self, value):
        return value.amount

    def to_internal_value(self, data):
        import decimal
        try:
            return decimal.Decimal(data)
        except:
            self.fail('incorrect_format')

