from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Dataset, DataItem
from rest_framework import serializers


class DatasetSerializer(serializers.ModelSerializer):
    total_items = serializers.SerializerMethodField()
    completed_items = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()
    label_classes = serializers.SerializerMethodField()

    class Meta:
        model = Dataset
        fields = ['id', 'name', 'file_type', 'status', 'label_classes',
                  'total_items', 'completed_items', 'progress_percent', 'created_at']

    def get_total_items(self, obj): return obj.total_items()
    def get_completed_items(self, obj): return obj.completed_items()
    def get_progress_percent(self, obj): return obj.progress_percent()
    def get_label_classes(self, obj): return obj.get_label_classes()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dataset_stats(request, pk):
    try:
        dataset = Dataset.objects.get(pk=pk)
    except Dataset.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)
    return Response(DatasetSerializer(dataset).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_datasets_stats(request):
    datasets = Dataset.objects.all() if request.user.is_admin() else Dataset.objects.filter(status='active')
    return Response(DatasetSerializer(datasets, many=True).data)
