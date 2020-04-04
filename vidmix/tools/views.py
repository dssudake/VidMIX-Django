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
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
""" -------- Audio Replace View -------- """
def replace(request, video_id, audio_id):
  # print("I am HEREREEEEEE")
  try:
    video = VideoUpload.objects.get(pk=video_id)
  except VideoUpload.DoesNotExist:
    raise Http404("Page Does not exist.")
  if request.method == "POST":
    data = {'success': "Successful !!", 'audioid': audio_id}
  else:
    data = {'success': "Error"}

  sub_replace = request.POST['subtitle']
  audio_replace = request.FILES['audio']
  audio_replace_url = settings.MEDIA_ROOT + str(video.id) + '/audio/replace/' + str(audio_id)
  fs = FileSystemStorage(audio_replace_url)
  filename = fs.save(audio_replace.name, audio_replace)
  uploaded_file_url = settings.MEDIA_ROOT + str(video.id) + '/audio/replace/' + str(audio_id) + '/' + filename
  time_start_end = settings.MEDIA_ROOT + str(video.id) + '/subtitle/' + '/tse.txt'
  with open(time_start_end) as fp:
    for i, line in enumerate(fp):
      if i == (audio_id - 1):
        res = tuple(map(str, line.split(', ')))
        end = res[2].rstrip()
        start = res[1]
  ip_audio = settings.MEDIA_ROOT + str(video.id) + '/audio' +"/audio.mp3"
  op_audio = settings.MEDIA_ROOT + str(video.id) + '/audio' +"/new.mp3"
  p1_audio = audio_replace_url + "/z1.mp3"
  os.system('ffmpeg -hide_banner -loglevel panic -i {} -ss {} -to {} {}'.format(ip_audio,0,start,p1_audio))
  p3_audio = audio_replace_url + "/z3.mp3"
  os.system('ffmpeg -hide_banner -loglevel panic -i {} -ss {}  {}'.format(ip_audio,end,p3_audio))
  os.system("ffmpeg -hide_banner -loglevel panic -i {} -i {} -i {} -filter_complex '[0:0][1:0][2:0]concat=n=3:v=0:a=1[out]' -map '[out]' {} ".format(p1_audio,uploaded_file_url,p3_audio,op_audio))

  ip_video = settings.MEDIA_ROOT + str(video.videofile)
  op_video = settings.MEDIA_ROOT + str(video.id) + '/video' +"/new.mp4"
  os.system("ffmpeg -hide_banner -loglevel panic -i {} -i {} -c:v copy -map 0:v:0 -map 1:a:0 {}".format(ip_video,op_audio,op_video))
  
  return JsonResponse(data)