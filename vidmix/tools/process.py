from django.conf import settings
from .models import VideoUpload
import os,webvtt, pysrt, time

""" -------- Audio Cropping -------- """
def audio_crop(video_id):
  video = VideoUpload.objects.get(pk=video_id)

  vtt = webvtt.from_srt(str(video.subfile.path))
  vtt.save()

  f = pysrt.open(str(video.subfile.path))
  time_start_end = settings.MEDIA_ROOT + str(video.id) + '/subtitle/' + '/tse.txt'
  file = open(time_start_end, "w")
  for i in range(len(f)):
    timestamp ="{}, {}:{}:{}.{}, {}:{}:{}.{}\n".format(
      i+1,
      f[i].start.hours,
      f[i].start.minutes,
      f[i].start.seconds,
      f[i].start.milliseconds,
      f[i].end.hours,
      f[i].end.minutes,
      f[i].end.seconds,
      f[i].end.milliseconds
    )
    file.write(timestamp)
  file.close()

  ip_video = settings.MEDIA_ROOT + str(video.videofile)
  os.system('mkdir {}'.format(settings.MEDIA_ROOT + str(video.id) + '/audio'))
  os.system('mkdir {}'.format(settings.MEDIA_ROOT + str(video.id) + '/audio/crop'))
  ip_audio = settings.MEDIA_ROOT + str(video.id) + '/audio' +"/audio.mp3"
  os.system('ffmpeg -hide_banner -i {} -vn {}'.format(ip_video,ip_audio))
  time.sleep(3)

  crop = open(time_start_end, "r")
  for line in crop: 
    res = tuple(map(str, line.split(', '))) 
    z = res[2].rstrip()
    op_audio = settings.MEDIA_ROOT + str(video.id) + '/audio/crop' + "/op_{}.mp3".format(res[0])
    os.system('ffmpeg -hide_banner -loglevel panic -i {} -ss {} -to {} {}'.format(ip_audio,res[1],z,op_audio))
    time.sleep(0.2)
  crop.close()


""" -------- Context generating -------- """
def context_generate(video_id):
  video = VideoUpload.objects.get(pk=video_id)
  subfile_path_vtt = str(video.subfile).replace("srt", "vtt")
  audio_path = str(video_id) + '/audio/crop'

  f = pysrt.open(str(video.subfile.path))
  table_data = []
  for i in range(len(f)):
    s_h = s_m = s_s = s_i = e_h = e_m = e_s = e_i = 0
    s_h = f[i].start.hours
    s_m = f[i].start.minutes
    s_s = f[i].start.seconds
    s_i = f[i].start.milliseconds
    e_h = f[i].end.hours
    e_m = f[i].end.minutes
    e_s = f[i].end.seconds
    e_i = f[i].end.milliseconds
    start_time = ((s_m * 60) + s_s) + (s_i/1000)
    end_time = ((e_m * 60) + e_s) + (e_i/1000)
    start_ts = "{} : {} : {}.{}".format(s_h,s_m,s_s,s_i)
    end_ts = "{} : {} : {}.{}".format(e_h,e_m,e_s,e_i)
    table_data.append((str(i+1),start_ts,end_ts,f[i].text,start_time,end_time))

  context = {
    'id' : video.id,
    'title' : video.name,
    'videofile' : video.videofile,
    'subfile' : subfile_path_vtt,
    'audio_path' : audio_path,
    'display': table_data,
    'nos' : range(len(table_data)),
  }
  return context