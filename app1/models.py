from django.db import models


# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=18)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    url = models.URLField()
    portal = models.ImageField(upload_to='img')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
