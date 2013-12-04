from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=10)
    password = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=20)
    abstract = models.CharField(max_length=100)
    notice = models.CharField(max_length=100)
    pic = models.CharField(max_length=50)
    category = models.CharField(max_length=20)
    publisher = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=200)
    date = models.DateTimeField('date published')
    publisher = models.ForeignKey(User)

    def __unicode__(self):
        return self.title

class SiteInfo(models.Model):
    category = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=200)
    publisher = models.ForeignKey(User)

    def __unicode__(self):
        return self.title