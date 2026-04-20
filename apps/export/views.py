import csv
import json
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from apps.datasets.models import Dataset
from apps.annotations.models import Annotation


def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin():
            messages.error(request, 'Admin access required.')
            return redirect('dashboard:home')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def export_dataset(request, dataset_pk, fmt):
    """Export annotated dataset as CSV or JSON."""
    dataset = get_object_or_404(Dataset, pk=dataset_pk)
    
    if not request.user.is_admin() and dataset.uploaded_by != request.user:
        messages.error(request, 'You do not have permission to export this dataset.')
        return redirect('datasets:detail', pk=dataset_pk)
    annotations = Annotation.objects.filter(
        data_item__dataset=dataset,
        data_item__is_corrupted=False,
        data_item__status='done'
    ).select_related('data_item', 'annotator', 'verified_by').order_by('data_item__order')

    rows = []
    for ann in annotations:
        item = ann.data_item
        rows.append({
            'item_id': item.pk,
            'file': item.file.url if item.file else '',
            'text_content': item.text_content or '',
            'label': ann.label or '',
            'bounding_boxes': json.dumps(ann.bounding_boxes) if fmt == 'csv' else (ann.bounding_boxes or []),
            'confidence': ann.confidence,
            'annotator': ann.annotator.username if ann.annotator else '',
            'verified': ann.verified,
            'verified_by': ann.verified_by.username if ann.verified_by else '',
            'labeled_at': ann.updated_at.isoformat() if ann.updated_at else '',
        })

    safe_name = dataset.name.replace(' ', '_').lower()

    if fmt == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{safe_name}_export.csv"'
        writer = csv.DictWriter(response, fieldnames=rows[0].keys() if rows else [])
        writer.writeheader()
        writer.writerows(rows)
        return response

    elif fmt == 'json':
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{safe_name}_export.json"'
        payload = {
            'dataset': dataset.name,
            'file_type': dataset.file_type,
            'label_classes': dataset.get_label_classes(),
            'total_items': len(rows),
            'exported_at': __import__('datetime').datetime.utcnow().isoformat() + 'Z',
            'items': rows,
        }
        json.dump(payload, response, indent=2)
        return response

    messages.error(request, 'Invalid export format. Use csv or json.')
    return redirect('datasets:detail', pk=dataset_pk)
