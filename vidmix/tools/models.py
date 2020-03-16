from django.db import models
import os

# Create your models here.

def get_video_path(instance, filename):
  return os.path.join(str(instance.id),'video',filename)

def get_sub_path(instance, filename):
  return os.path.join(str(instance.id),'subtitle',filename)

class VideoUpload(models.Model):
  name = models.CharField(verbose_name="Title", max_length=500)
  videofile = models.FileField(upload_to=get_video_path, null=True, verbose_name="Video")
  subfile = models.FileField(upload_to=get_sub_path, null=True, verbose_name="Subtitle")

  def __str__(self):
    return self.name + ": " + str(self.videofile)