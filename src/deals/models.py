from django.db import models

# Create your models here.

class Deal(models.Model):
    title = models.CharField(max_length=120, default="")
    image = models.ImageField()
    url = models.TextField()

    def __str__(self):
        return self.title