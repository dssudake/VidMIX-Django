# Generated by Django 3.0.1 on 2020-03-16 14:46

from django.db import migrations, models
import tools.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VideoUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Title')),
                ('videofile', models.FileField(null=True, upload_to=tools.models.get_video_path, verbose_name='Video')),
                ('subfile', models.FileField(null=True, upload_to=tools.models.get_sub_path, verbose_name='Subtitle')),
            ],
        ),
    ]
