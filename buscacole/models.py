from django.db import models
from escuelas.models import Grade, Level
# Create your models here.
class Search(models.Model):
    criteria = models.CharField(max_length=100, blank=False)

class SearchDetail(models.Model):
    search = models.ForeignKey('Search', on_delete=models.CASCADE, blank=False)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=False)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, blank=False)
