from django.contrib import admin
from .models import Annotation, AuditLog

@admin.register(Annotation)
class AnnotationAdmin(admin.ModelAdmin):
    list_display = ['id', 'data_item', 'annotator', 'label', 'verified', 'created_at']
    list_filter = ['verified']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'annotation', 'changed_by', 'old_label', 'new_label', 'timestamp']
    readonly_fields = ['timestamp']
