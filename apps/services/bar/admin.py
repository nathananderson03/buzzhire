from django.contrib import admin
from apps.job.admin import JobRequestAdmin
from apps.freelancer.admin import FreelancerAdmin
from apps.paygrade.admin import PayGradeAdmin
from . import models


class BarFreelancerAdmin(FreelancerAdmin):
    list_display = FreelancerAdmin.list_display + ('role',)

admin.site.register(models.BarFreelancer, BarFreelancerAdmin)


class BarJobRequestAdmin(JobRequestAdmin):
    list_display = JobRequestAdmin.list_display + ('role',)

admin.site.register(models.BarJobRequest, BarJobRequestAdmin)

class BarPayGradeAdmin(PayGradeAdmin):
    list_display = ('role',) + PayGradeAdmin.list_display
    list_filter = PayGradeAdmin.list_filter + ('role',)

admin.site.register(models.BarPayGrade, BarPayGradeAdmin)
