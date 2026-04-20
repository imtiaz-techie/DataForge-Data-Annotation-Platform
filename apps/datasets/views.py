import os
import zipfile
import mimetypes
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Dataset, DataItem
from .forms import DatasetForm, DataItemTextForm


def admin_required(view_func):
    """Decorator: only admins can access this view."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin():
            messages.error(request, 'Admin access required.')
            return redirect('dashboard:home')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def dataset_list(request):
    if request.user.is_admin():
        datasets = Dataset.objects.all()
    else:
        # Annotators see active datasets and datasets they uploaded
        datasets = Dataset.objects.filter(Q(status='active') | Q(uploaded_by=request.user)).distinct()
    return render(request, 'datasets/dataset_list.html', {'datasets': datasets})


@login_required
def dataset_detail(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    items = dataset.items.all()
    context = {
        'dataset': dataset,
        'items': items,
        'total': dataset.total_items(),
        'done': dataset.completed_items(),
        'pending': dataset.pending_items(),
        'corrupted': dataset.items.filter(is_corrupted=True).count(),
        'progress': dataset.progress_percent(),
    }
    return render(request, 'datasets/dataset_detail.html', context)


@login_required
def dataset_upload(request):
    form = DatasetForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        dataset = form.save(commit=False)
        dataset.uploaded_by = request.user
        dataset.save()

        # Handle file uploads
        uploaded_files = request.FILES.getlist('files')
        text_items = request.POST.get('text_items', '').strip()
        order = 0

        # Process ZIP files
        for f in uploaded_files:
            if f.name.lower().endswith('.zip'):
                order = _process_zip(dataset, f, order)
            elif dataset.file_type == 'text' and f.name.lower().endswith(('.txt', '.csv')):
                content = f.read().decode('utf-8', errors='replace')
                for line in content.splitlines():
                    line = line.strip()
                    if line:
                        DataItem.objects.create(dataset=dataset, text_content=line, order=order)
                        order += 1
            else:
                valid, reason = _validate_file(f, dataset.file_type)
                if valid:
                    item = DataItem(dataset=dataset, file=f, order=order)
                    item.save()
                    order += 1
                else:
                    item = DataItem(dataset=dataset, file=f, is_corrupted=True,
                                    corruption_reason=reason, order=order)
                    item.save()
                    order += 1

        # Process text items (newline-separated)
        if text_items and dataset.file_type == 'text':
            for i, line in enumerate(text_items.splitlines()):
                line = line.strip()
                if line:
                    DataItem.objects.create(dataset=dataset, text_content=line, order=order + i)

        messages.success(request, f'Dataset "{dataset.name}" created with {dataset.total_items()} items.')
        return redirect('datasets:detail', pk=dataset.pk)

    return render(request, 'datasets/upload.html', {'form': form})


def _validate_file(f, file_type):
    """Return (is_valid, reason). Checks size and MIME type."""
    max_size = 50 * 1024 * 1024  # 50MB
    if f.size > max_size:
        return False, 'File exceeds 50MB limit'
    mime, _ = mimetypes.guess_type(f.name)
    if file_type == 'image':
        if not mime or not mime.startswith('image/'):
            return False, f'Not an image file (detected: {mime})'
    if file_type == 'text':
        allowed_text = ['text/plain', 'text/csv', 'application/json']
        if not mime or mime not in allowed_text:
            return False, f'Not a supported text file (detected: {mime})'
    return True, ''


def _process_zip(dataset, zip_file, start_order):
    """Extract and process files from a ZIP archive. Returns next order int."""
    order = start_order
    try:
        with zipfile.ZipFile(zip_file, 'r') as zf:
            for name in zf.namelist():
                if name.endswith('/'):
                    continue
                with zf.open(name) as f:
                    from django.core.files.base import ContentFile
                    content = f.read()
                    basename = os.path.basename(name)
                    ext = basename.lower().split('.')[-1]
                    if dataset.file_type == 'image' and ext in ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp']:
                        item = DataItem(dataset=dataset, order=order)
                        item.file.save(basename, ContentFile(content), save=True)
                        order += 1
                    elif dataset.file_type == 'text' and ext in ['txt', 'csv']:
                        text_content = content.decode('utf-8', errors='replace')
                        for line in text_content.splitlines():
                            line = line.strip()
                            if line:
                                DataItem.objects.create(dataset=dataset, text_content=line, order=order)
                                order += 1
    except zipfile.BadZipFile:
        pass
    return order


@login_required
def dataset_edit(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    
    if not request.user.is_admin() and dataset.uploaded_by != request.user:
        messages.error(request, 'You do not have permission to edit this dataset.')
        return redirect('datasets:detail', pk=pk)
        
    form = DatasetForm(request.POST or None, instance=dataset)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Dataset updated.')
        return redirect('datasets:detail', pk=pk)
    return render(request, 'datasets/edit.html', {'form': form, 'dataset': dataset})


@login_required
@require_POST
def dataset_delete(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    
    if not request.user.is_admin() and dataset.uploaded_by != request.user:
        messages.error(request, 'You do not have permission to delete this dataset.')
        return redirect('datasets:list')
        
    dataset.delete()
    messages.success(request, 'Dataset deleted.')
    return redirect('datasets:list')


@login_required
@require_POST
def mark_corrupted(request, item_pk):
    item = get_object_or_404(DataItem, pk=item_pk)
    
    if not request.user.is_admin() and item.dataset.uploaded_by != request.user:
        messages.error(request, 'You do not have permission to modify this item.')
        return redirect('datasets:detail', pk=item.dataset.pk)
    item.is_corrupted = not item.is_corrupted
    reason = request.POST.get('reason', 'Manually marked by admin')
    item.corruption_reason = reason if item.is_corrupted else ''
    item.save()
    messages.success(request, f"Item {'marked as corrupted' if item.is_corrupted else 'restored'}.")
    return redirect('datasets:detail', pk=item.dataset.pk)
