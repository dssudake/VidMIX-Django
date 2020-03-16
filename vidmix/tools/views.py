from django.shortcuts import render

# Create your views here.
def home(request):
  return render(request , 'tools/home.html')

def about(request):
  return render(request , 'tools/about.html')

def contact(request):
  return render(request , 'tools/contact.html')