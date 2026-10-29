from django.db import models

# Create your models here.

from django.conf import settings
from django.db import models


class Member(models.Model):

    class MemberType(models.TextChoices):
        FIRST_TIMER = "first_timer", "First Timer"
        MEMBER = "member", "Church Member"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        TRANSFERRED = "transferred", "Transferred"

    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)

    member_type = models.CharField(
        max_length=20,
        choices=MemberType.choices,
        default=MemberType.FIRST_TIMER,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    first_visit_date = models.DateField(null=True, blank=True)
    date_joined_church = models.DateField(null=True, blank=True)
    church_group = models.CharField(max_length=100, blank=True)

    # Respect members' communication preferences.
    contact_consent = models.BooleanField(default=False)

    notes = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="registered_members",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name
