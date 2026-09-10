import os
from django.db import models

# Dynamic upload paths based on issue_date year
def stamp_upload_path(instance, filename):
    year = instance.issue_date.year
    return os.path.join(str(year), "stamps", filename)

def fdc_upload_path(instance, filename):
    year = instance.issue_date.year
    return os.path.join(str(year), "first_day_covers", filename)

def brochure_upload_path(instance, filename):
    year = instance.issue_date.year
    return os.path.join(str(year), "brochures", filename)

class Stamp(models.Model):
    name = models.CharField(max_length=200)
    issue_date = models.DateField()
    denomination = models.CharField(max_length=50)
    theme = models.CharField(max_length=200)
    keywords = models.TextField(blank=True, help_text="Comma separated keywords")
    description = models.TextField(blank=True)

    # Images stored yearwise in subfolders
    image = models.ImageField(upload_to=stamp_upload_path, blank=True, null=True)
    first_day_cover = models.ImageField(upload_to=fdc_upload_path, blank=True, null=True)
    brochure_image1 = models.ImageField(upload_to=brochure_upload_path, blank=True, null=True)
    brochure_image2 = models.ImageField(upload_to=brochure_upload_path, blank=True, null=True)

    def __str__(self):
        return self.name


class Year(models.Model):
    year = models.IntegerField(unique=True)
    image = models.ImageField(upload_to='year_images/', blank=True, null=True)

    def __str__(self):
        return str(self.year)
