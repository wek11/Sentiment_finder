from django.db import models

# Create your models here.

class Link(models.Model):
    link_url = models.CharField(max_length=300)

    text = models.CharField(max_length=100000, default="")

    def __str__(self):
        return self.link_url
    
    def reset_id(self):
        links = self.objects.all()
        index = 1
        for link in links:
            link.id = index
    
class Data(models.Model):
    text = models.CharField(max_length=10000)

    def __str__(self):
        return self.text
