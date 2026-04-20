import json
from django.db import models
from django.conf import settings


class Dataset(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('completed', 'Completed'),
    ]
    FILE_TYPE_CHOICES = [
        ('image', 'Image'),
        ('text', 'Text'),
    ]
    TASK_CHOICES = [
        ('classification', 'Classification'),
        ('object_detection', 'Object Detection'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    label_classes = models.JSONField(default=list, help_text='List of label class names e.g. ["cat","dog"]')
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='image')
    annotation_task = models.CharField(max_length=30, choices=TASK_CHOICES, default='classification')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='datasets'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def total_items(self):
        return self.items.count()

    def completed_items(self):
        return self.items.filter(status='done').count()

    def pending_items(self):
        return self.items.filter(status='pending').count()

    def progress_percent(self):
        total = self.total_items()
        if total == 0:
            return 0
        return round((self.completed_items() / total) * 100, 1)

    def get_label_classes(self):
        if isinstance(self.label_classes, list):
            return self.label_classes
        try:
            return json.loads(self.label_classes)
        except Exception:
            return []


class DataItem(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='items')
    file = models.FileField(upload_to='dataset_items/', blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_corrupted = models.BooleanField(default=False)
    corruption_reason = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"Item #{self.pk} - {self.dataset.name}"

    def filename(self):
        if self.file:
            return self.file.name.split('/')[-1]
        return None

    def is_image(self):
        if self.file:
            ext = self.file.name.lower().split('.')[-1]
            return ext in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp']
        return False
