from django.contrib import admin


class PayGradeAdmin(admin.ModelAdmin):
    "Base ModelAdmin for PayGrades."
    list_display = ('years_experience',
                    'min_client_pay_per_hour')
