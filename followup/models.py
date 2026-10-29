from django.db import models

# Create your models here.

from django.conf import settings
from django.db import models


class FollowUp(models.Model):

    class Reason(models.TextChoices):
        FIRST_TIMER = "first_timer", "First Timer"
        ABSENCE = "absence", "Missed Service"
        BIRTHDAY = "birthday", "Birthday"
        GENERAL = "general", "General Check-in"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        NORMAL = "normal", "Normal"
        HIGH = "high", "High"

    member = models.ForeignKey(
        "members.Member",
        on_delete=models.PROTECT,
        related_name="followups",
    )

    reason = models.CharField(
        max_length=20,
        choices=Reason.choices,
    )

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.NORMAL,
    )

    due_date = models.DateField()

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_followups",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_followups",
    )

    outcome = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["due_date", "-priority"]

    def __str__(self):
        return f"{self.title} - {self.member.full_name}"


class FollowUpInteraction(models.Model):

    class InteractionType(models.TextChoices):
        PHONE_CALL = "phone_call", "Phone Call"
        WHATSAPP = "whatsapp", "WhatsApp"
        SMS = "sms", "SMS"
        IN_PERSON = "in_person", "In Person"
        EMAIL = "email", "Email"

    followup = models.ForeignKey(
        FollowUp,
        on_delete=models.CASCADE,
        related_name="interactions",
    )

    interaction_type = models.CharField(
        max_length=20,
        choices=InteractionType.choices,
    )

    summary = models.TextField()
    contacted_at = models.DateTimeField()
    response_received = models.BooleanField(default=False)

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="followup_interactions",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-contacted_at"]

    def __str__(self):
        return f"{self.interaction_type} - {self.followup.member.full_name}"
