from django.db import models

class SchoolImage(models.Model):
    IMAGE_TYPE_CHOICES = (
        ('banner', 'Banner/Hero'),
        ('gallery', 'Gallery'),
        ('facility', 'Facility'),
    )
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='school/')  # → S3 mein jayegi
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPE_CHOICES, default='gallery')
    order = models.IntegerField(default=0)  # sequence control
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.image_type} - {self.title}"

