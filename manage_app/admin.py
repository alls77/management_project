from django.contrib import admin

from .models import Company, Manager, Work, Worker, Workplace, WorkTime, Statistics


admin.site.register(Company)
admin.site.register(Manager)
admin.site.register(Work)
admin.site.register(Worker)
admin.site.register(Workplace)
admin.site.register(WorkTime)
admin.site.register(Statistics)
