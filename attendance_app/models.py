from django.db import models

# Create your models here.

from django.conf import settings
from django.db import models


class ChurchService(models.Model):

    class ServiceType(models.TextChoices):
        SUNDAY = "sunday", "Sunday Service"
        MIDWEEK = "midweek", "Midweek Service"
        SPECIAL = "special", "Special Service"

    title = models.CharField(max_length=150)
    service_type = models.CharField(
        max_length=20,
        choices=ServiceType.choices,
        default=ServiceType.SUNDAY,
    )
    service_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_services",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-service_date", "-start_time"]

    def __str__(self):
        return f"{self.title} - {self.service_date}"


class AttendanceRecord(models.Model):

    class AttendanceStatus(models.TextChoices):
        PRESENT = "present", "Present"
        ABSENT = "absent", "Absent"
        EXCUSED = "excused", "Excused"

    member = models.ForeignKey(
        "members.Member",
        on_delete=models.PROTECT,
        related_name="attendance_records",
    )

    service = models.ForeignKey(
        ChurchService,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )

    status = models.CharField(
        max_length=10,
        choices=AttendanceStatus.choices,
    )

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recorded_attendance",
    )

    notes = models.CharField(max_length=255, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["member__full_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["member", "service"],
                name="unique_member_attendance_per_service",
            )
        ]

    def __str__(self):
        return (
            f"{self.member.full_name} - "
            f"{self.service.title}: {self.status}"
        )
