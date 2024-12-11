from django.contrib import admin

from driven.db.mail.models import MailDBO


class MailAdmin(admin.ModelAdmin):
    pass


admin.site.register(MailDBO, MailAdmin)
