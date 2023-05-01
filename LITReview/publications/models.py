from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image

RATING_ON = "★"
RATING_OFF = "☆"
RATING_RANGE = range(5)


class Ticket(models.Model):
    """Class for a standard ticket"""

    title = models.CharField(max_length=128, verbose_name="title")
    description = models.TextField(
        max_length=2048, blank=True, verbose_name="description"
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    image = models.ImageField(null=True, blank=True, verbose_name="image")
    time_created = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)

    IMAGE_MAX_SIZE = (600, 600)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()


class Review(models.Model):
    """Class for a standard review"""

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, null=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], null=True
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    headline = models.CharField(
        max_length=128, blank=True, verbose_name="headline"
    )
    body = models.TextField(max_length=8192, blank=True, verbose_name="body")
    time_created = models.DateTimeField(auto_now_add=True)
