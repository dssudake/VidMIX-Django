from django.urls import path

from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('contact/', views.contact, name='contact'),
]


# Add URLConf for video Upload and Edit views
urlpatterns += [
  path('tools/' , views.tools , name='tools'),
  path('tools/edit/<int:video_id>' , views.edit , name='edit'),
  path('upload/<int:video_id>/<int:audio_id>/', views.replace , name='replace'),
]