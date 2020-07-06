from django.db import models
from django.conf import settings
# Create your models here.

# model -- headline (title, image, url)
# model -- userprofile(user, last_scrape)

# only scrape once every while and store in a profile

class coronavirusCount(models.Model):
    virusCount = models.TextField()

    def __str__(self):
        return self.virusCount

class Headline(models.Model):
    title = models.CharField(max_length=120, default="")
    image = models.ImageField()
    url = models.TextField()
    description = models.CharField(max_length=240, default="")
    dateText = models.CharField(max_length=120, default="")

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    # grab the user model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_scrape = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{}-{}".format(self.user, self.last_scrape)