from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from models import Message, Problem, PublicUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.core import serializers
from cStringIO import StringIO
import sys
from django.utils import timezone


def user(request, username):
	if User.objects.filter(username=username).exists():
		context = {'user_id': User.objects.get(username=username).id, 'username': username}
		return render(request, 'user.html', context)
	else:
		return render(request, 'main_page.html')

@csrf_exempt 
def am_i_watched(request):
	user_id = request.POST.get('user_id')
	if PublicUser.objects.filter(user_id=user_id).exists():
		public_user = PublicUser.objects.get(user_id=user_id)
		if(request.POST.get('text') != ''):
			public_user.text = request.POST.get('text')
			public_user.save()
		last_time = public_user.last_watched
		if timezone.now() - last_time < datetime.timedelta(seconds=5):
			return HttpResponse('True')
	else:
		new_public = PublicUser(user=request.user, last_watched=timezone.now())
		new_public.save()
	return HttpResponse('False')

@csrf_exempt
def get_user_code(request):
	user_id = request.POST.get('user_id')
	print user_id
	if PublicUser.objects.filter(user_id=user_id).exists():
		public_user = PublicUser.objects.get(user_id=user_id)
		public_user.last_watched = timezone.now()
		public_user.save()
		return HttpResponse(public_user.text)
	return HttpResponse('False')

# Create your views here.
def index(request):
	if(request.user.is_authenticated):
		return render(request, 'main_page.html')
	else:
		return render(request, 'main_page.html')

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
def get_python_output(request):
	code = request.POST.get('code')
	print code
	old_stdout = sys.stdout
	redirected_output = sys.stdout = StringIO()
	try:
		exec(code)
	except Exception as e:
		print str(e)
	sys.stdout = old_stdout
	json_output = json.dumps(redirected_output.getvalue())
	return HttpResponse(redirected_output.getvalue())

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

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


@csrf_exempt
def get_problem(request):
	problem_number = request.POST.get('problem_number')
	problem_data = Problem.objects.get(pk=problem_number)
	print problem_data.problem_text
	return HttpResponse(problem_data.problem_text)