from django import forms

from .models import VideoUpload

class VideoUploadForm(forms.ModelForm):
    name = forms.CharField(label='Title',widget=forms.TextInput(
        attrs={
            'class' : 'form-control',
            'placeholder' : 'Write a video title ...',           
        }
    ))
    class Meta:
        model = VideoUpload
        fields = ['name', 'videofile', 'subfile']