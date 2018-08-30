from django.db import models

# Create your models here.
class main(models.Model):
    image = models.URLField()
    content = models.TextField()
    hashtag = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    comment = models.CharField(max_length=100)
    like = models.CharField(max_length=10)