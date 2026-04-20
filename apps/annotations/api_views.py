from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone
from apps.datasets.models import DataItem, Dataset
from .models import Annotation, AuditLog


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_next_task(request, dataset_pk):
    """API: atomically get next available task for annotator."""
    try:
        dataset = Dataset.objects.get(pk=dataset_pk)
    except Dataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=404)

    from .views import _get_next_item, _release_expired_locks, _acquire_lock
    _release_expired_locks()
    item = _get_next_item(dataset, request.user)

    if not item:
        return Response({'status': 'complete', 'message': 'All items labeled'})

    annotation, _ = _acquire_lock(item, request.user)
    if annotation is None:
        return Response({'status': 'locked', 'message': 'Item locked by another user'})

    return Response({
        'status': 'assigned',
        'item_id': item.pk,
        'item_type': 'image' if item.is_image() else 'text',
        'file_url': item.file.url if item.file else None,
        'text_content': item.text_content,
        'label_classes': dataset.get_label_classes(),
        'existing_label': annotation.label,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_submit_label(request, item_pk):
    """API: submit a label for an item."""
    try:
        item = DataItem.objects.get(pk=item_pk)
    except DataItem.DoesNotExist:
        return Response({'error': 'Item not found'}, status=404)

    label = request.data.get('label', '').strip()
    confidence = int(request.data.get('confidence', 3))

    if not label:
        return Response({'error': 'Label required'}, status=400)

    valid_labels = item.dataset.get_label_classes()
    if valid_labels and label not in valid_labels:
        return Response({'error': 'Invalid label'}, status=400)

    with transaction.atomic():
        annotation, _ = Annotation.objects.get_or_create(data_item=item)
        old_label = annotation.label
        annotation.label = label
        annotation.confidence = confidence
        annotation.annotator = request.user
        annotation.locked_by = None
        annotation.locked_at = None
        annotation.save()
        item.status = 'done'
        item.save(update_fields=['status'])
        if old_label and old_label != label:
            AuditLog.objects.create(
                annotation=annotation, changed_by=request.user,
                old_label=old_label, new_label=label
            )

    return Response({'status': 'saved', 'label': label, 'item_id': item.pk})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_annotations(request):
    """API: get current user's annotation history."""
    annotations = Annotation.objects.filter(annotator=request.user).select_related('data_item', 'data_item__dataset')
    data = [{
        'id': a.pk,
        'dataset': a.data_item.dataset.name,
        'item_id': a.data_item.pk,
        'label': a.label,
        'confidence': a.confidence,
        'verified': a.verified,
        'created_at': a.created_at.isoformat(),
    } for a in annotations[:50]]
    return Response({'annotations': data, 'total': annotations.count()})
