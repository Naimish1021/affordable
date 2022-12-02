from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import *
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.utils.text import slugify
class IndexView(ListView):
	template_name='index.html'
	context_object_name='list'
	def get_queryset(self):
		return Blog.objects.all().values('state').distinct().order_by('state')

# def index(request):
# 	list = Blog.objects.all().values('state').distinct().order_by('state')
# 	return render(request,'index.html',{'list':list})

# def city(request,state):
# 	state=state.replace('-',' ')
# 	list = Blog.objects.filter(state__icontains=state).distinct().order_by('city')
# 	return render(request,'state.html',{'state':list[0].state,'list':list})

class CityView(ListView):
	template_name = 'state.html'
	context_object_name = 'list'
	def get_queryset(self,**kwargs):
		state = self.kwargs['state'].replace('-',' ')

		return Blog.objects.filter(state__icontains=state).distinct().order_by('city')
	

class BlogDetailView(DetailView):
	model = Blog
	template_name='content.html'
	context_object_name='blog'
	slug_field = 'slug'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		alts = Blog.objects.filter(state=self.object.state,id__gt=self.object.id).order_by('city')[:20]
		if len(alts) < 20 < len(Blog.objects.filter(state=self.object.state)):
			alts=(alts|Blog.objects.filter(state=self.object.state).order_by('city')[:20-len(alts)]).distinct()
		context["alts"] = alts
		return context
	
# def details(request,slug):
# 	key = Blog.objects.get(slug=slug)
# 	alts = Blog.objects.filter(state=key.state,id__gt=key.id).order_by('city')[:20]
# 	if len(alts) < 20 < len(Blog.objects.filter(state=key.state)):
# 		alts=(alts|Blog.objects.filter(state=key.state).order_by('city')[:20-len(alts)]).distinct()
	

# 	return render(request,'content.html',{'blog':key,'alts':alts})

# def contact_us(request):
# 	return render(request,'contact-us.html')

def city_list():
	for i in Blog.objects.all().values('state').distinct().order_by('state'):
		yield {'state':slugify(i['state'])}

def blog_list():
	for i in Blog.objects.all():
		yield {'slug':i.slug}