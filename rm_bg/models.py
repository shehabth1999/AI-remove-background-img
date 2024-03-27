from django.db import models

class ProcessedImage(models.Model):
    image = models.ImageField(upload_to='images/receved/')
    result_image = models.ImageField(upload_to='images/processed/', blank=True, null=True)


    def __str__(self) -> str:
        return self.image.name
