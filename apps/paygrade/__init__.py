"""The paygrade app controls the minimum rates for different kinds of
job requests.  It defines admin-editable models that can be used to control
these paygrades, depending on the service, and fields on the job request.

It also provides the ability for services to extend the PayGradeModel and
add custom logic.
"""
