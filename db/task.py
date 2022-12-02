import openai
from time import sleep
from .models import *

import psycopg2 
from django.template.defaultfilters import slugify 
import re
from celery import shared_task

KEYS = ['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']
Expired_key =[]
MAX_KEY_COUNT = len(KEYS)
KEYS_COUNT = 0

			

def gpt3(stext, key_count=0):

	global KEYS_COUNT,MAX_KEY_COUNT,Expired_key
	try:
		openai.api_key = KEYS[key_count]  
		response = openai.Completion.create(
				engine="text-davinci-002",
				prompt=stext,
				temperature=0.8,
				max_tokens=3020,
				top_p=1,
				frequency_penalty=0,
				presence_penalty=0

		)
		sleep(1)
		return response.choices[0].text
	
	except openai.error.RateLimitError as e:
		print(e,'and current key :',KEYS[key_count])	
		sleep(20)	
		KEYS_COUNT = (KEYS_COUNT+1)%MAX_KEY_COUNT
		return gpt3(stext, KEYS_COUNT)

	except  openai.error.AuthenticationError :
		Expired_key.append(KEYS[key_count])
		KEYS.remove(KEYS[key_count])
		MAX_KEY_COUNT = len(KEYS)
		sleep(5)	
		KEYS_COUNT = (KEYS_COUNT+1)%MAX_KEY_COUNT
		return gpt3(stext, KEYS_COUNT)

	except IndexError:
		print('all below keys are expired \n',Expired_key)
		

def get_data(state,city):
	global KEYS_COUNT,MAX_KEY_COUNT,Expired_key
	k = 'Homeless assistance '
	key,created = Blog.objects.get_or_create(name=k,slug = slugify(f'{k}-{city}-{state}'),city=slugify(city),state=slugify(state))
	if created:
		query = f'Generate Blog topic ideas for "{k} in {city} ,{ state}" \n*'
		qqs = gpt3(query,KEYS_COUNT)
		KEYS_COUNT = (KEYS_COUNT+1)%MAX_KEY_COUNT
		list = re.split('[\*\-\#]',qqs.strip())
		content = ''
		if len(list) <= 2:
			list = re.split(r'\d+[.)]',re.sub(r'^[\*\-\#]','',qqs.strip()))
		for i in list:
			if i.strip() != '':
				q= re.sub('(?<!\d)^\d+[.)]|^\s*\d+[.)](?<!\d)','',i.strip())
				query = f'Write Blog section : {i}'
				aa = gpt3(query,KEYS_COUNT).replace('\n','<br>')
				KEYS_COUNT = (KEYS_COUNT+1)%MAX_KEY_COUNT
				content +=f'<h2>{q}</h2><p>{aa}<p>'
		key.body=content
		key.save()		
		
def get_by_id(id):
	conn = psycopg2.connect(
   	host="45.56.94.45",
	database="gmap",
	user="postgres",
	password="popanda",
	port =5432           
	)

	cur = conn.cursor()

	sql = f'SELECT  "city"."name", "state"."name" FROM "city" INNER JOIN "state" ON ("city"."state_id" = "state"."id") where "city"."id" = {str(id)}'
	cur.execute(sql)
	data = cur.fetchone()
	get_data(data[1],data[0])
	cur.close()
	
@shared_task()
def Generate_blog(list):
	print(list)
	global KEYS_COUNT,MAX_KEY_COUNT,Expired_key
	for key in list:
		blog,created = Blog.objects.get_or_create(name=key,slug = slugify(key))
		
		if created:
			query = f'Generate Blog topic ideas for "{key} " \n*'
			qqs = gpt3(query,KEYS_COUNT)
			KEYS_COUNT = (KEYS_COUNT+1)%MAX_KEY_COUNT
			list = re.split('[\*\-\#]',qqs.strip())
			content = ''
			if len(list) <= 2:
				list = re.split(r'\d+[.)]',re.sub(r'^[\*\-\#]','',qqs.strip()))
			for i in list:
				if i.strip() != '':
					q= re.sub('(?<!\d)^\d+[.)]|^\s*\d+[.)](?<!\d)','',i.strip())
					query = f'Write Blog section : {i}'
					aa = gpt3(query,KEYS_COUNT).replace('\n','<br>')
					KEYS_COUNT = (KEYS_COUNT+1)%MAX_KEY_COUNT
					content +=f'<h2>{q}</h2><p>{aa}<p>'
			blog.body=content
			blog.save()	