from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return HttpResponse("TIME TO CHAT IT UP.")

def chat(request):
	return render(request, 'chat.html')

def send_message(request):
	return render(request, 'chat.html')