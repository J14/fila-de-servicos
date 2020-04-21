from django.contrib import admin, messages

from . import models
from . import forms


class QueueAdmin(admin.ModelAdmin):
    list_filter = ('service',)
    form = forms.QueueForm


class ServiceAdmin(admin.ModelAdmin):
    actions = ('attendance',)

    def attendance(self, request, queryset):
        for service in queryset:
            att = service.queue.first()

            if att is not None:
                att.attending = False
                att.attended = True
                att.save()
                self.message_user(
                    request,
                    "Person attended in queue {}".format(service)
                )

                att = service.queue.first()
                if att is not None:
                    att.attending = True
                    att.save()
            else:
                self.message_user(
                    request,
                    "Nobody waiting in queue {}".format(service),
                    level=messages.WARNING
                )


admin.site.register(models.Person)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.Queue, QueueAdmin)
