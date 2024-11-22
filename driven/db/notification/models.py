from django.db import models
from django.utils.translation import gettext_lazy as _

from driven.db.user.models import UserDBO


class DeviceDBO(models.Model):
    device_id = models.CharField(max_length=255, verbose_name=_("Device ID"))
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        UserDBO, on_delete=models.CASCADE, related_name="devices"  # Cambié "user" por "devices"
    )
    PLATFORMS = (
        ("ios", _("iOS")),
        ("android", _("Android")),
    )
    platform = models.CharField(
        max_length=10, verbose_name=_("Platform"), choices=PLATFORMS
    )

    class Meta:
        verbose_name = _("Dispositivo")
        verbose_name_plural = _("Dispositivos")

    def __str__(self) -> str:
        return f"{self.device_id} - {self.user_id}"


class NotificationDBO(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    data = models.JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        UserDBO, on_delete=models.CASCADE, related_name='created_notifications'  # Cambié "notifications" por "created_notifications"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Notificación")
        verbose_name_plural = _("Notificaciones")

    def __str__(self):
        return self.title


class UserNotificationDBO(models.Model):
    user = models.ForeignKey(
        UserDBO, on_delete=models.CASCADE, related_name='received_notifications'  # Cambié "notifications" por "received_notifications"
    )
    notification = models.ForeignKey(
        NotificationDBO, on_delete=models.CASCADE, related_name='user_notifications'
    )
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Notificación a usuario")
        verbose_name_plural = _("Notificaciones a usuarios")
        unique_together = ('user', 'notification')


    def __str__(self):
        return f"Notification to {self.user.email}: {self.notification.title}"

