from django.contrib.sitemaps import Sitemap
from .models import Blog

class BlogSiteMap(Sitemap):
    limit = 50000

    def items(self):
        return Blog.objects.all()
    
    def location(self,obj):
        return f'/city/{obj.slug}'

