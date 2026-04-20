from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.views.decorators.http import require_POST
from apps.datasets.models import DataItem, Dataset
from .models import Annotation, AuditLog


@login_required
def label_item(request, item_pk):
    """Main labeling view — handles both image and text items."""
    item = get_object_or_404(DataItem, pk=item_pk)

    if item.is_corrupted:
        messages.warning(request, 'This item is marked as corrupted and cannot be labeled.')
        return redirect('datasets:detail', pk=item.dataset.pk)

    # Acquire or verify lock
    annotation, created = _acquire_lock(item, request.user)
    if annotation is None:
        messages.error(request, 'This item is currently being labeled by another annotator. Please try another item.')
        return redirect('annotations:queue', dataset_pk=item.dataset.pk)

    label_classes = item.dataset.get_label_classes()
    if item.is_image():
        if item.dataset.annotation_task == 'object_detection':
            template = 'annotations/label_bounding_box.html'
        else:
            template = 'annotations/label_image.html'
    else:
        template = 'annotations/label_text.html'

    context = {
        'item': item,
        'annotation': annotation,
        'label_classes': label_classes,
        'dataset': item.dataset,
        'existing_label': annotation.label if annotation.label else '',
    }
    return render(request, template, context)


@login_required
@require_POST
def submit_label(request, item_pk):
    """Submit or update a label for a data item."""
    item = get_object_or_404(DataItem, pk=item_pk)
    label = request.POST.get('label', '').strip()
    confidence = request.POST.get('confidence', 3)

    is_obj_detection = item.dataset.annotation_task == 'object_detection'
    
    if not is_obj_detection:
        if not label:
            messages.error(request, 'Please select a label.')
            return redirect('annotations:label_item', item_pk=item_pk)

        valid_labels = item.dataset.get_label_classes()
        if valid_labels and label not in valid_labels:
            messages.error(request, 'Invalid label selected.')
            return redirect('annotations:label_item', item_pk=item_pk)

    with transaction.atomic():
        annotation, _ = Annotation.objects.get_or_create(data_item=item)
        old_label = annotation.label
        old_boxes = annotation.bounding_boxes

        if is_obj_detection:
            import json
            boxes_data = request.POST.get('bounding_boxes', '[]')
            try:
                annotation.bounding_boxes = json.loads(boxes_data)
            except Exception:
                annotation.bounding_boxes = []
        else:
            annotation.label = label
            
        annotation.confidence = int(confidence)
        annotation.annotator = request.user
        annotation.locked_by = None
        annotation.locked_at = None
        annotation.save()

        # Update item status
        item.status = 'done'
        item.save(update_fields=['status'])

        # Audit log (only for classification right now for simplicity)
        if not is_obj_detection and old_label and old_label != label:
            AuditLog.objects.create(
                annotation=annotation,
                changed_by=request.user,
                old_label=old_label,
                new_label=label,
                note='Label updated by annotator'
            )

    messages.success(request, f'Label "{label}" saved successfully!')
    # Go to next item
    next_item = _get_next_item(item.dataset, request.user)
    if next_item:
        return redirect('annotations:label_item', item_pk=next_item.pk)
    else:
        messages.info(request, 'All items in this dataset have been labeled! Great job!')
        return redirect('datasets:detail', pk=item.dataset.pk)


@login_required
def annotation_queue(request, dataset_pk):
    """Show the annotator their task queue for a dataset."""
    dataset = get_object_or_404(Dataset, pk=dataset_pk)
    # Release any expired locks
    _release_expired_locks()

    next_item = _get_next_item(dataset, request.user)
    if next_item:
        return redirect('annotations:label_item', item_pk=next_item.pk)
    else:
        items = dataset.items.filter(status='done').select_related('annotation')
        context = {'dataset': dataset, 'items': items, 'all_done': True}
        return render(request, 'annotations/queue_complete.html', context)


@login_required
def review_annotations(request, dataset_pk):
    """Admin or uploader only: review and verify all annotations."""
    dataset = get_object_or_404(Dataset, pk=dataset_pk)
    if not request.user.is_admin() and dataset.uploaded_by != request.user:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    annotations = Annotation.objects.filter(data_item__dataset=dataset).select_related(
        'data_item', 'annotator', 'verified_by'
    )
    return render(request, 'annotations/review.html', {
        'dataset': dataset,
        'annotations': annotations,
    })


@login_required
@require_POST
def verify_annotation(request, annotation_pk):
    """Admin or uploader verifies or overrides an annotation."""
    annotation = get_object_or_404(Annotation, pk=annotation_pk)
    if not request.user.is_admin() and annotation.data_item.dataset.uploaded_by != request.user:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')
    new_label = request.POST.get('label', '').strip()
    action = request.POST.get('action', 'verify')

    old_label = annotation.label

    if action == 'override' and new_label:
        annotation.label = new_label
        AuditLog.objects.create(
            annotation=annotation,
            changed_by=request.user,
            old_label=old_label,
            new_label=new_label,
            note='Label overridden by admin'
        )

    annotation.verified = True
    annotation.verified_by = request.user
    annotation.verified_at = timezone.now()
    annotation.save()

    messages.success(request, 'Annotation verified.')
    return redirect('annotations:review', dataset_pk=annotation.data_item.dataset.pk)


@login_required
@require_POST
def release_lock(request, item_pk):
    """Release lock on an item (annotator abandons task)."""
    item = get_object_or_404(DataItem, pk=item_pk)
    try:
        ann = item.annotation
        if ann.locked_by == request.user:
            ann.release_lock()
            if item.status == 'in_progress':
                item.status = 'pending'
                item.save(update_fields=['status'])
    except Annotation.DoesNotExist:
        pass
    return redirect('datasets:detail', pk=item.dataset.pk)


# ─── Helpers ────────────────────────────────────────────────────────────────

def _acquire_lock(item, user):
    """
    Atomically acquire or validate a lock on a data item.
    Returns (annotation, created) or (None, False) if locked by another user.
    """
    from django.conf import settings
    timeout = settings.ANNOTATION_LOCK_TIMEOUT

    with transaction.atomic():
        annotation, created = Annotation.objects.select_for_update().get_or_create(
            data_item=item,
            defaults={'label': '', 'annotator': user}
        )
        now = timezone.now()

        if annotation.locked_by and annotation.locked_by != user:
            # Check if lock expired
            if annotation.locked_at:
                expiry = annotation.locked_at + timezone.timedelta(minutes=timeout)
                if now < expiry:
                    return None, False  # Still locked by another user

        # Acquire / renew lock
        annotation.locked_by = user
        annotation.locked_at = now
        annotation.save(update_fields=['locked_by', 'locked_at'])

        # Mark item as in_progress
        if item.status == 'pending':
            item.status = 'in_progress'
            item.save(update_fields=['status'])

    return annotation, created


def _get_next_item(dataset, user):
    """Get the next unlabeled, unlocked item for this user."""
    from django.conf import settings
    timeout = settings.ANNOTATION_LOCK_TIMEOUT
    expire_threshold = timezone.now() - timezone.timedelta(minutes=timeout)

    # Items not done, not corrupted, not locked by another user
    candidates = dataset.items.filter(
        status__in=['pending', 'in_progress'],
        is_corrupted=False
    ).order_by('order', 'id')

    for item in candidates:
        try:
            ann = item.annotation
            # Skip if locked by another user and lock not expired
            if ann.locked_by and ann.locked_by != user:
                if ann.locked_at and ann.locked_at > expire_threshold:
                    continue
        except Annotation.DoesNotExist:
            pass
        return item
    return None


def _release_expired_locks():
    """Release all expired annotation locks."""
    from django.conf import settings
    timeout = settings.ANNOTATION_LOCK_TIMEOUT
    expire_threshold = timezone.now() - timezone.timedelta(minutes=timeout)

    Annotation.objects.filter(
        locked_by__isnull=False,
        locked_at__lt=expire_threshold
    ).update(locked_by=None, locked_at=None)

    # Reset in_progress items with expired locks
    DataItem.objects.filter(
        status='in_progress',
    ).filter(
        annotation__locked_by__isnull=True
    ).update(status='pending')
