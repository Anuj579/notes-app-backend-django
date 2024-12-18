from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
import cloudinary


# Create your models here.
class Note(models.Model):

    CATEGORY = (
        ("BUSINESS", "Business"),
        ("PERSONAL", "Personal"),
        ("IMPORTANT", "Important"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY, default="PERSONAL")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_base = slugify(self.title)
            slug = slug_base

            # Check if the slug is unique and modify it if necessary
            if Note.objects.filter(slug=slug).exists():
                slug = f"{slug_base}-{get_random_string(5)}"
            self.slug = slug
        super(Note, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = CloudinaryField("image", blank=True, null=True)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return ""

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
