from django.contrib import admin
from .models import Dataset, DataItem

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['name', 'file_type', 'status', 'uploaded_by', 'created_at']
    list_filter = ['file_type', 'status']
    search_fields = ['name']

@admin.register(DataItem)
class DataItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'dataset', 'status', 'is_corrupted', 'created_at']
    list_filter = ['status', 'is_corrupted']
