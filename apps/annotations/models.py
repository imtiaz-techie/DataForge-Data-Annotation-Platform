from django.db import models
from django.conf import settings
from django.utils import timezone


class Annotation(models.Model):
    CONFIDENCE_CHOICES = [(i, str(i)) for i in range(1, 6)]

    data_item = models.OneToOneField(
        'datasets.DataItem',
        on_delete=models.CASCADE,
        related_name='annotation'
    )
    annotator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='annotations'
    )
    label = models.CharField(max_length=255, null=True, blank=True)
    bounding_boxes = models.JSONField(null=True, blank=True, help_text="Stores array of bounding boxes: [{'label':'x','x':0,'y':0,'w':0,'h':0}]")
    confidence = models.IntegerField(choices=CONFIDENCE_CHOICES, default=3)

    # Concurrency lock
    locked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='locked_annotations'
    )
    locked_at = models.DateTimeField(null=True, blank=True)

    # Verification
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_annotations'
    )
    verified_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Annotation #{self.pk} - {self.label}"

    def is_locked(self):
        if not self.locked_by or not self.locked_at:
            return False
        timeout = settings.ANNOTATION_LOCK_TIMEOUT
        expiry = self.locked_at + timezone.timedelta(minutes=timeout)
        return timezone.now() < expiry

    def release_lock(self):
        self.locked_by = None
        self.locked_at = None
        self.save(update_fields=['locked_by', 'locked_at'])


class AuditLog(models.Model):
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE, related_name='audit_logs')
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    old_label = models.CharField(max_length=255, blank=True)
    new_label = models.CharField(max_length=255)
    note = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"AuditLog #{self.pk}: {self.old_label} -> {self.new_label}"
