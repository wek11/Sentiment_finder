from django.db import models

# Create your models here.

# Link model, stores the url and text associated with a given link, and 
# has a method to reset the id's when a link is a modified
class Link(models.Model):
    link_url = models.CharField(max_length=300)

    text = models.CharField(max_length=100000, default="")

    def __str__(self):
        return self.link_url
    
    @staticmethod
    def reset_id(self):
        links = self.objects.all()
        index = 0
        for link in links:
            link.id = index
            index += 1

