from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from learnrapp.models import Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login
from django.core import serializers


# Create your views here.
def index(request):
	return render(request, 'main_page.html')
	#return HttpResponse("TIME TO CHAT IT UP.")


def chat(request):
	messages = Message.objects.all()
	context = {'messages' : messages}
	return render(request, 'chat.html', context)

@csrf_exempt 
def get_messages(request):
	last_message_id = request.POST.get('latest_message')
	if int(last_message_id) == -1:
		new_messages = Message.objects.filter(id__gt=last_message_id).values('id','text','sender').order_by('-id')[:5]
		for message in new_messages:
			message['name'] = User.objects.get(pk=message['sender']).username;
	elif last_message_id != None:
		new_messages = Message.objects.filter(id__gt=last_message_id).values('id','text','sender').order_by('-id')
		for message in new_messages:
			message['name'] = User.objects.get(pk=message['sender']).username;
	else:
		new_messages = {'status': 'no'}
	json_messages = json.dumps(list(new_messages))
	return HttpResponse(json_messages)

@csrf_exempt      
def send_message(request):
	#http://lethain.com/two-faced-django-part-5-jquery-ajax/
	results = {'success':False}
	if request.method == u'POST':
		results = {'success':'fff'}
		POST = request.POST
		if POST.has_key(u'text'):
			results = {'heck':'here'}
			text = POST[u'text']
			message = Message(sender=request.user, text=text, time=datetime.datetime.now())
			message.save();
	json_results = json.dumps(results)
	return HttpResponse(json_results)

def register(request):
	if request.method == 'POST':
		username = username=request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		User.objects.create_user(username=username, email=email, password=password)
		return HttpResponseRedirect('/')
	else:
		return render(request, 'register.html')

def login(request):
	if request.method == 'POST':
		username = username=request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			auth_login(request, user)
			return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/')
	else:
		return render(request, 'login.html')