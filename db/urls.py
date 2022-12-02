from django.urls import path

from .views import *
from django.contrib.sitemaps import views as site_map
from .sitemap import *
from .feed import BlogFeed
from django_distill import distill_path

sitemaps={
    'blog':BlogSiteMap,
}
def st():
    yield {'section':'blog'}
urlpatterns = [
    distill_path('',IndexView.as_view(),name='index'),
    # distill_path('sitemap.xml',site_map.index, {'sitemaps': sitemaps},
    #      name='django.contrib.sitemaps.views.index'),
     distill_path('sitemap-<section>.xml',
         (site_map.sitemap),
         {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap',distill_func=st),
    distill_path('state/<str:state>/',CityView.as_view(),name='city-list',distill_func=city_list),
    distill_path('city/<slug:slug>/',BlogDetailView.as_view(),name='detail',distill_func=blog_list),
    # path('contact-us/',contact_us),
    distill_path('feed/',BlogFeed(),name='feed')
]
