
from django.db import models
from tinymce.models import HTMLField



class Blog(models.Model):
    name = models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    slug = models.SlugField()
    body = HTMLField()
    nextpage=HTMLField(null=True,blank=True)
    class Meta:
        unique_together = ('slug', 'city','state')
    
    def __str__(self) -> str:
        return self.name + self.city

    class Meta:
        db_table = 'blog'


class Place(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=70)
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=250,default="NA")
    pincode = models.CharField(max_length=20,default="NA")
    phone = models.CharField(max_length=30,default="NA")
    rating = models.FloatField(default=0)
    reviews = models.IntegerField(default=0)
    website = models.CharField(max_length=250,null=True,blank=True)
    time = models.TextField(null=True,blank=True)
    type = models.ForeignKey(Blog,related_name='places',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
