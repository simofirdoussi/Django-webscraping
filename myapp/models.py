from django.db import models

class Search(models.Model):

    search = models.CharField(max_length=400)
    max_price = models.CharField(max_length=400)
    min_price = models.CharField(max_length = 400)
    # category = models.CharField(max_length=400)
    # city = models.CharField(max_length=400)

    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.search)
        return '{}'.format(self.max_price)
        return '{}'.format(self.min_price)
        return '{}'.format(self.category)
        return '{}'.format(self.city)
        
       







