from django.contrib import admin

from driven.db.notification.models import DeviceDBO, NotificationDBO, UserNotificationDBO


class NotificationAdmin(admin.ModelAdmin):
    pass


admin.site.register(DeviceDBO, NotificationAdmin)
admin.site.register(NotificationDBO, NotificationAdmin)
admin.site.register(UserNotificationDBO, NotificationAdmin)