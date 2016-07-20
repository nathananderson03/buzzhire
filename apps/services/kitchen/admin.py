from django.contrib import admin
from apps.job.admin import JobRequestAdmin
from apps.freelancer.admin import FreelancerAdmin
from apps.paygrade.admin import PayGradeAdmin
from . import models


class KitchenFreelancerAdmin(FreelancerAdmin):
    list_display = FreelancerAdmin.list_display + ('role',)

admin.site.register(models.KitchenFreelancer, KitchenFreelancerAdmin)


class KitchenJobRequestAdmin(JobRequestAdmin):
    list_display = JobRequestAdmin.list_display + ('role',)

admin.site.register(models.KitchenJobRequest, KitchenJobRequestAdmin)


class KitchenPayGradeAdmin(PayGradeAdmin):
    list_display = ('role',) + PayGradeAdmin.list_display
    list_filter = PayGradeAdmin.list_filter + ('role',)

admin.site.register(models.KitchenPayGrade, KitchenPayGradeAdmin)
