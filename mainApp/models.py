from django.db import models
from PIL import Image
from django.conf import settings
import os

# Create your models here.
class ImageUp(models.Model):
    img=models.ImageField(upload_to='uploads/')
    desired_width=models.IntegerField()
    desired_height=models.IntegerField()
    upload_date=models.DateTimeField(auto_now_add=True)
    is_resized=models.BooleanField(default=False)

    def resize(self):
        img = Image.open(self.img.path)
        img = img.resize((self.desired_width, self.desired_height))
        resized_img_path = os.path.join(settings.MEDIA_ROOT, 'uploads', f'resized_{self.img.name}')
        img.save(resized_img_path)
        self.is_resized = True
        self.save()