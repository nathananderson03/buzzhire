import calendar
from .models import Availability
from apps.job.models import JobRequest
from apps.freelancer.models import Freelancer, client_to_freelancer_rate
from apps.job import service_from_class


class JobMatcher(object):
    """The workhorse for matching freelancers to job requests, or from a form.

    Usage:
        matcher = JobMatcher(job_request)
        freelancers = matcher.get_results()
    Or:
        matcher = JobMatcher(job_request, cleaned_data)
        freelancers = matcher.get_results()
    """
    flat_fields = ('date', 'client_pay_per_hour', 'years_experience')

    def __init__(self, job_request, cleaned_data=None):
        # We always need to know what job request we're searching for,
        # so we can determine the correct kind of freelancer
        self.job_request = job_request

        if cleaned_data:
            # Sets the search terms from the cleaned_data from a form
            self.search_terms = cleaned_data
        else:
            self.set_search_terms_from_job_request()


    def set_search_terms_from_job_request(self):
        self.search_terms = {}

        # Set initial for flat fields (i.e. ones that directly map between
        # form and job request attributes)
        for field in self.flat_fields:
            self.search_terms[field] = getattr(self.job_request, field)

        # Other fields
        self.search_terms['raw_postcode'] = str(self.job_request.postcode)
        self.search_terms['shift'] = Availability.shift_from_time(
                                                self.job_request.start_time)


    def get_results(self, ignore_availability=False):
        """Returns the freelancers that match the search terms.
        Optionally, can ignore the availability provided by the freelancers.
        """

        service = service_from_class(self.job_request.__class__)
        result_class = service.freelancer_model
        results = result_class.published_objects.all()

        results = self.filter_by_years_experience(results)
        if not ignore_availability:
            results = self.filter_by_availability(results)
        results = self.filter_by_pay_per_hour(results)
        results = self.filter_by_location(results)

        # Return unique results
        return results.distinct()


    def filter_by_years_experience(self, results):
        "Filters by minimum years of experience."
        if self.search_terms['years_experience']:
            results = results.filter(
                years_experience__gte=self.search_terms['years_experience'])
        return results


    def filter_by_availability(self, results):
        "Filters by availability, if it's been searched for."

        if self.search_terms['date']:

            # Get day of week for that date
            day_name = calendar.day_name[
                                self.search_terms['date'].weekday()].lower()

            # Build filter kwargs
            field_name = '%s_%s' % (day_name, self.search_terms['shift'])
            filter_kwargs = {'availability__%s' % field_name: True}

            # Filter
            results = results.filter(**filter_kwargs)

        return results

    def filter_by_pay_per_hour(self, results):
        """Filters the results based on the minimum pay per hour.
        This also sets self.freelancer_pay_per_hour in case client code
        needs to know it.
        """

        if self.search_terms['client_pay_per_hour']:
            self.freelancer_pay_per_hour = client_to_freelancer_rate(
                                    self.search_terms['client_pay_per_hour'])
            return results.filter(
                        minimum_pay_per_hour__lte=self.freelancer_pay_per_hour)
        return results

    def filter_by_location(self, results):
        """Filters the results by the supplied postcode, checking that it's
        within an acceptable distance for the driver."""
        if self.search_terms.get('postcode'):
            # Specific include distances so the template knows
            self.include_distances = True
            searched_point = self.search_terms['postcode'].point
            results = results.distance(searched_point,
                                       field_name='postcode__point')\
                        .order_by('distance')

            # if self.search_terms['respect_travel_distance']:
                # Filter by only those drivers whose travel distance works
                # with the postcode supplied
                # TODO - get this working with their personal distance settings
                # http://stackoverflow.com/questions/9547069/geodjango-distance-filter-with-distance-value-stored-within-model-query
                # results = results.filter(
                #      postcode__point__distance_lte=(searched_point, D(mi=4)))

        return results
