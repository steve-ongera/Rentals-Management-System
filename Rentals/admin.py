from django.contrib import admin
from .models import *

admin.site.register(Month)
admin.site.register(Profile)
admin.site.register(Payment_Year)
admin.site.register(House)
admin.site.register(Tenant)
admin.site.register(tenants_database)
admin.site.register(MonthlySignOff)
admin.site.register(Payment)
admin.site.register(MaintenanceRequest)
admin.site.register(QnAResponse)
admin.site.register(Worker)
admin.site.register(NonStaff)
admin.site.register(LeaveNotice)
admin.site.register(Booking)

admin.site.site_header='Ngeka Rentals '
admin.site.site_title='Kikuyu | App'
admin.site.index_title='Welcome to Ngeka'
