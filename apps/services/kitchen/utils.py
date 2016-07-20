from apps.booking.utils import JobMatcher


class KitchenJobMatcher(JobMatcher):
    "JobMatcher tailored to matching kitchen staff."

    flat_fields = JobMatcher.flat_fields + ('role',)

    def get_results(self, *args, **kwargs):
        results = super(KitchenJobMatcher, self).get_results(*args, **kwargs)
        results = self.filter_by_role(results)
        return results

    def filter_by_role(self, results):
        "Filters by role."

        if self.search_terms['role']:
            return results.filter(
                            role=self.search_terms['role'])

        return results
