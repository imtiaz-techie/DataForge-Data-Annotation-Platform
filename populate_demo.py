import os
import django
import zipfile
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dataforge.settings')
django.setup()

from apps.datasets.models import Dataset, DataItem
from django.contrib.auth import get_user_model

User = get_user_model()
admin_user, _ = User.objects.get_or_create(username='admin', defaults={'is_superuser': True, 'is_staff': True})

dataset = Dataset.objects.create(
    name='Demo Vehicles Dataset',
    description='A dataset to test object detection.',
    file_type='image',
    annotation_task='object_detection',
    label_classes=['Car', 'Bus', 'Person', 'Tie'],
    uploaded_by=admin_user,
    status='active'
)

# Unzip and add to dataset
zip_path = 'car_dataset.zip'
if os.path.exists(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        extract_dir = 'temp_extraction'
        zip_ref.extractall(extract_dir)
        
        for root, _, files in os.walk(extract_dir):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    item = DataItem(dataset=dataset)
                    item.file.save(file, File(f))
                    item.save()

print('Successfully created Demo Dataset!')
