from django.db import models
from django.utils.text import slugify
from django.urls import reverse

import misaka

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    level = models.ManyToManyField('Level' ,blank=False)
    specialization = models.ManyToManyField('Specialization', blank=True)
    address = models.TextField(max_length=255, blank=False) #TODO Mäs de una dirección
    phone = models.TextField(max_length=255, blank=False)   #TODO Mäs de un teléfono
    email = models.EmailField()                             #TODO Mäs de un mail
    web = models.URLField()
    shifts = models.ManyToManyField('Shift', blank=True)
    religion = models.ManyToManyField('Religion', blank=True)
    connected_school = models.ManyToManyField('School', blank=True)
    activity = models.ManyToManyField('Activity', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("schools:single", kwargs={"slug": self.slug})


    class Meta:
        ordering = ["name"]


class Level(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Specialization(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Shift(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Religion(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Activity(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]