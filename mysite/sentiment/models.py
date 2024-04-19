from django.db import models

# Create your models here.

class Link(models.Model):
    link_url = models.CharField(max_length=300)

    def __str__(self):
        return self.link_url
    
class Data(models.Model):
    text = models.CharField(max_length=10000)

    def __str__(self):
        return self.text
