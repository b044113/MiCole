from django.db import models
from django.utils.text import slugify
from django.urls import reverse

#import misaka

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    level = models.ManyToManyField('Level' ,blank=False)
    specialization = models.ManyToManyField('Specialization', blank=True)
    address = models.TextField(max_length=255, blank=False) #TODO Mäs de una dirección
    post_code  = models.CharField(max_length=10, blank=False, null=True)
    province = models.ForeignKey('Province', on_delete=models.SET_NULL, null=True)  # models.CASCADE
    locality = models.ForeignKey('Locality', on_delete=models.SET_NULL, null=True)  # models.CASCADE
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True, blank=True)  # models.CASCADE
    phone = models.TextField(max_length=255, blank=False)   #TODO Mäs de un teléfono
    email = models.EmailField(blank=True)                             #TODO Mäs de un mail
    web = models.URLField(blank=True)
    shifts = models.ManyToManyField('Shift', blank=True)

    RELIGIONS = (
        ('l', 'Laico'),
        ('c', 'Católico'),
        ('j', 'Judío'),
        ('e', 'Evangélico'),
    )

    religion = models.CharField(max_length=1, choices=RELIGIONS, blank=True, default='l',
                              help_text='Orientación religiosa')

    connected_school = models.ManyToManyField('School', blank=True)
    activity = models.ManyToManyField('Activity', blank=True)
    #TODO agregar barrio, localidad, provincia y georreferencia

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = self.description #misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("escuelas:school-detail", args=[str(self.id)])


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

class Activity(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class Province(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Locality(models.Model):
    name = models.CharField(max_length=50, unique=True)
    province = models.ForeignKey('Province', on_delete=models.CASCADE, blank=False) #models.SET_NULL

    def __str__(self):
        return ''.join([self.name, ", ", self.province.name])

    class Meta:
        ordering = ["name"]


class City(models.Model):
    name = models.CharField(max_length=50, unique=True)
    locality = models.ForeignKey('Locality', on_delete=models.CASCADE, blank=False) #models.SET_NULL

    def __str__(self):
        return ''.join([self.name, ", ", self.locality.__str__()])

    class Meta:
        ordering = ["name"]

class Vacancy(models.Model):
    school = models.ForeignKey('School', on_delete=models.CASCADE, blank=False)
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE, blank=False)
    vacancies = models.IntegerField(blank=False)

    def __str__(self):
        return ''.join([self.school.name, ', ', self.grade.name, ": ", str(self.vacancies)])

class Grade(models.Model):
    name = models.CharField(max_length=30, unique=True)
    level = models.ForeignKey('Level', on_delete=models.CASCADE)

    def __str__(self):
        return ''.join([self.name, ', ', self.level.name])

    class Meta:
        ordering = ["name"]