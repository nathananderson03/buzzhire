import braintree
from braintree.exceptions.not_found_error import NotFoundError
from django.conf import settings
import logging


logger = logging.getLogger('project')


class PaymentException(Exception):
    "A payment-specific exception."
    pass


class PaymentAPI(object):
    """Used to handle calls to Braintree.
    """

    def __init__(self):
        # Set sandbox / production server depending on BRAINTREE_SANDBOX mode
        environment = braintree.Environment.Sandbox \
                        if settings.BRAINTREE_SANDBOX \
                        else braintree.Environment.Production
        braintree.Configuration.configure(
                environment,
                merchant_id=settings.BRAINTREE_MERCHANT_ID,
                public_key=settings.BRAINTREE_PUBLIC_KEY,
                private_key=settings.BRAINTREE_PRIVATE_KEY)


    def generate_client_token(self, person):
        """Generates a client-side token for the supplied user.
        Note that the 'client token' is the browser/front end,
        rather than apps.client.models.Client.
        
        Arguments:
               person - Any model, such as apps.client.models.Client, that
                        has the following attributes:
                           1. reference_number - a unique identifier
                              for the person
                           2. first_name
                           3. last_name
                           4. phone
                           5. user - a link to the user
        """
        customer = self.get_or_create_customer(person)
        return braintree.ClientToken.generate({
            "customer_id": customer.id
        })

    def get_or_create_customer(self, person):
        """Returns a braintree customer object for the supplied person
        - will create one if it doesn't already exist.
        """
        try:
            return braintree.Customer.find(person.reference_number)
        except NotFoundError:
            result = braintree.Customer.create({
                "id": person.reference_number,
                "first_name": person.first_name,
                "last_name": person.last_name,
                "email": person.user.email,
                "phone": person.mobile,
            })
            if not result.is_success:
                raise PaymentException(
                                'Could not create customer for %s.' % person)
            else:
                return result.customer

    def take_payment(self, payment_method_nonce, amount, order_id):
        """Take a payment from a person.
        
        Arguments:
            payment_method_nonce: Supplied client-side.
            amount: Decimal of the amount to charge, in GBP.
            order_id: The order id to store in Braintree.  Generally
                      should be the job request reference number.
        """
        result = braintree.Transaction.sale({
                "amount": amount,
                "payment_method_nonce": payment_method_nonce,
                "order_id": order_id,
        })
        if not result.is_success:
            logger.error('Payment error: %s' % \
                            [e for e in result.errors.deep_errors])
            raise PaymentException('Could not take payment.')
        return result
