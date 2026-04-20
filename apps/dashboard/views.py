from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.datasets.models import Dataset, DataItem
from apps.annotations.models import Annotation
from apps.accounts.models import CustomUser


@login_required
def home(request):
    if request.user.is_admin():
        return admin_dashboard(request)
    return annotator_dashboard(request)


def admin_dashboard(request):
    datasets = Dataset.objects.all()
    total_datasets = datasets.count()
    total_items = DataItem.objects.count()
    total_annotated = DataItem.objects.filter(status='done').count()
    total_corrupted = DataItem.objects.filter(is_corrupted=True).count()
    total_users = CustomUser.objects.filter(role='annotator').count()
    total_verified = Annotation.objects.filter(verified=True).count()
    overall_progress = round((total_annotated / total_items * 100), 1) if total_items else 0

    # Annotator leaderboard
    from django.db.models import Count
    leaderboard = CustomUser.objects.filter(role='annotator').annotate(
        count=Count('annotations')
    ).order_by('-count')[:10]

    # Recent datasets
    recent_datasets = datasets.order_by('-created_at')[:5]

    context = {
        'total_datasets': total_datasets,
        'total_items': total_items,
        'total_annotated': total_annotated,
        'total_corrupted': total_corrupted,
        'total_users': total_users,
        'total_verified': total_verified,
        'overall_progress': overall_progress,
        'leaderboard': leaderboard,
        'recent_datasets': recent_datasets,
        'datasets': datasets,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


def annotator_dashboard(request):
    user = request.user
    my_annotations = Annotation.objects.filter(annotator=user)
    total_labeled = my_annotations.count()
    verified_count = my_annotations.filter(verified=True).count()
    active_datasets = Dataset.objects.filter(status='active')

    # Count pending items per dataset
    datasets_with_pending = []
    for ds in active_datasets:
        pending = ds.items.filter(status__in=['pending', 'in_progress'], is_corrupted=False).count()
        datasets_with_pending.append({
            'dataset': ds,
            'pending': pending,
            'total': ds.total_items(),
            'done': ds.completed_items(),
            'progress': ds.progress_percent(),
        })

    # Recent activity
    recent = my_annotations.select_related('data_item__dataset').order_by('-updated_at')[:10]

    context = {
        'total_labeled': total_labeled,
        'verified_count': verified_count,
        'datasets_with_pending': datasets_with_pending,
        'recent': recent,
    }
    return render(request, 'dashboard/annotator_dashboard.html', context)
