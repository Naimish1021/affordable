from django.contrib.syndication.views import Feed
from .models import Blog
from django.utils.feedgenerator import Rss201rev2Feed


class BlogFeed(Feed):
    title = 'Homeless Assistance Programs'
    link = '/'
    feed_type = Rss201rev2Feed
    language='en'
    def items(self):
        return Blog.objects.order_by('-id')[:1560]

    def item_title(self, item) :
        return f'{item.name}in {item.city}, {item.state}'
    
    def item_link(self, item):
        return f'/city/{item.slug}'