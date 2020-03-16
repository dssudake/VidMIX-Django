from django.shortcuts import render

# Create your views here.
def home(request):
  return render(request , 'tools/home.html')

def about(request):
  return render(request , 'tools/about.html')

def contact(request):
  return render(request , 'tools/contact.html')

from django.http import Http404,HttpResponseRedirect
from django.urls import reverse

from .process import audio_crop
from .models import VideoUpload
from .forms import VideoUploadForm

""" -------- Video Upload Handel -------- """
def tools(request):
  if request.method == 'POST':
    form = VideoUploadForm(request.POST,request.FILES)
    if form.is_valid():
      video = VideoUpload.objects.create()
      video.name = request.POST.get('name')
      video_file = request.FILES.get('videofile')
      sub_file = request.FILES.get('subfile')
      video.videofile.save(video_file.name, video_file)
      video.subfile.save(sub_file.name, sub_file)
      audio_crop(video.id)
      return HttpResponseRedirect(reverse("edit", args=(video.id,)))
      
  else:
    form = VideoUploadForm()

  context = {
    'form': form
  }
  return render(request , 'tools/tools.html' , context)


from .process import context_generate

""" -------- Video Editing View -------- """
def edit(request, video_id):
  try:
    video = VideoUpload.objects.get(pk=video_id)
  except VideoUpload.DoesNotExist:
    raise Http404("Page Does not exist.")

  context = context_generate(video_id)

  return render(request , 'tools/edit.html' , context)


from django.http import JsonResponse
""" -------- Audio Replace View -------- """
def replace(request):
  print("I am HEREREEEEEE")
  if request.method == "POST":
    data = {'success': "Successful Submission"}
  else:
    data = {'success': "Error"}
  print(data)
  print(request.POST['subtitle'])
  print(str(request.FILES['audio']))
  print(JsonResponse(data))
  return JsonResponse(data)