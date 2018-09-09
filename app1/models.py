from django.db import models


# Create your models here.

class Author(models.Model):
    author_sex = (
        ('M', '男'),
        ('F', '女'),
    )
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=18)
    sex = models.CharField(max_length=1, choices=author_sex)

    def __str__(self):
        return self.name


class AuthorDetail(models.Model):
    LEVEL = (
        ('NORMAL', '普通会员'),
        ('VIP', 'VIP会员'),
    )
    level = models.CharField(max_length=10, choices=LEVEL)
    author = models.OneToOneField(Author, on_delete=models.CASCADE)


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    url = models.URLField()
    portal = models.ImageField(upload_to='img')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class Publisher(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=50)
    author = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=10)

    def __str__(self):
        return self.name
