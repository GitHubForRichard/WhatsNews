from django.conf import settings
from django.db import models

# Create your models here.

class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)

    description = models.CharField(max_length=360)

    # means you can leave this field blank
    image = models.ImageField(null=True, blank=True)

    # means you can leave this field blank but title is mandatory
    url = models.URLField(null=True, blank=True)

    # means the moment it creates will be filled with this field
    timestamp = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     app_label = 'dashboard.model'

    # define which title it should show as the string title
    def __str__(self):
        return self.title
    #   return self.url

    def get_delete_url(self):
        return "/notes/{}/delete".format(self.pk)

    def get_update_url(self):
        return "/notes/{}/update".format(self.pk)

