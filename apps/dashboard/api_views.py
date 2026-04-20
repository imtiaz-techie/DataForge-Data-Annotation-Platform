from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.datasets.models import Dataset, DataItem
from apps.annotations.models import Annotation
from apps.accounts.models import CustomUser
from django.db.models import Count


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    if request.user.is_admin():
        data = {
            'total_datasets': Dataset.objects.count(),
            'total_items': DataItem.objects.count(),
            'total_annotated': DataItem.objects.filter(status='done').count(),
            'total_corrupted': DataItem.objects.filter(is_corrupted=True).count(),
            'total_users': CustomUser.objects.filter(role='annotator').count(),
            'total_verified': Annotation.objects.filter(verified=True).count(),
        }
    else:
        user = request.user
        data = {
            'total_labeled': Annotation.objects.filter(annotator=user).count(),
            'verified': Annotation.objects.filter(annotator=user, verified=True).count(),
        }
    return Response(data)
