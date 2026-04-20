import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dataforge.settings')
django.setup()

from apps.datasets.models import Dataset, DataItem
from apps.accounts.models import CustomUser
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw
import io

def create_sample_text_dataset(admin_user):
    print("Creating Text Dataset...")
    ds = Dataset.objects.create(
        name="Customer Reviews Sentiment",
        description="A sample dataset containing customer reviews that need to be classified as Positive, Neutral, or Negative.",
        file_type='text',
        label_classes='Positive, Neutral, Negative',
        uploaded_by=admin_user
    )
    
    reviews = [
        "The product quality is excellent! I absolutely love it.",
        "It's okay, nothing special but it gets the job done.",
        "Terrible experience, it broke after two days of use.",
        "Very fast shipping and great customer service. 5 stars!",
        "The color is a bit different from the picture, but acceptable.",
        "I wouldn't recommend this to anyone. Waste of money.",
        "Exactly what I was looking for. Perfect fit.",
        "The battery life is decent, could be better.",
        "Worst purchase ever. Do not buy!",
        "Highly recommended, will definitely buy again."
    ]
    
    for text in reviews:
        DataItem.objects.create(
            dataset=ds,
            text_content=text,
            status='pending'
        )
    print(f"Created text dataset with {len(reviews)} items.")

def create_sample_image_dataset(admin_user):
    print("Creating Image Dataset...")
    ds = Dataset.objects.create(
        name="Traffic Sign Classification",
        description="Identify the type of traffic sign in the generated dummy images.",
        file_type='image',
        label_classes='Speed Limit, Stop Sign, Yield, No Entry',
        uploaded_by=admin_user
    )
    
    # Generate dummy images using Pillow
    colors = ['#ef4444', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4']
    texts = ['SPEED 50', 'STOP', 'YIELD', 'NO ENTRY', 'SPEED 80', 'PARKING']
    
    for i, color in enumerate(colors):
        img = Image.new('RGB', (400, 400), color=color)
        draw = ImageDraw.Draw(img)
        # Draw a simple shape in the middle just for looks
        draw.ellipse((50, 50, 350, 350), outline="white", width=10)
        draw.text((160, 190), texts[i], fill="white")
        
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG')
        img_content = ContentFile(img_io.getvalue(), name=f'sign_{i}.jpg')
        
        DataItem.objects.create(
            dataset=ds,
            file=img_content,
            status='pending'
        )
    print(f"Created image dataset with {len(colors)} sample images.")

def run():
    admin_user = CustomUser.objects.filter(username='admin').first()
    if not admin_user:
        print("Admin user not found. Please create it first.")
        return
        
    if Dataset.objects.count() == 0:
        create_sample_text_dataset(admin_user)
        create_sample_image_dataset(admin_user)
        print("Sample data populated successfully! Refresh your browser.")
    else:
        print("Database already contains datasets. Skipping sample generation.")

if __name__ == '__main__':
    run()
