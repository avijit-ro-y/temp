from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    #work db
    #data transfer
    return HttpResponse("Welcome to task management system")

def show_task(request):
    return HttpResponse("This is taskpage")