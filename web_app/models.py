from django.db import models
from django.conf import settings
from django.contrib import admin
from PIL import Image
import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from web_app.azure_storage import AzureMediaStorage as AMS

# Create your models here.
class Connect(models.Model):
    name=models.CharField(max_length=255, null=True,blank=True)
    email=models.EmailField(max_length=255,null=True,blank=True)
    number=models.CharField(max_length=255,null=True,blank=True)
    messages=models.TextField(null=True,blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="Connect"

class VideoLink(models.Model):
    # video_url = models.FileField(upload_to='videos', null=True, blank=True, verbose_name="Video")
    # background_url = models.FileField(upload_to='videos', null=True, blank=True, verbose_name="Background Image")
    # link=models.CharField(max_length=255, null=True, blank=True)

    video_url = models.FileField(upload_to='videos', storage=AMS, null=True, blank=True)
    background_url = models.FileField(upload_to='videos', null=True, blank=True, verbose_name="Background Image")
    link=models.CharField(max_length=255, null=True, blank=True)
    
    # def __str__(self):
    #     return self.link

    class Meta:
        verbose_name_plural="VideoLink"

    def __str__(self):
        return 'VideoLink #{}'.format(self.id)
    
    # def save(self, *args, **kwargs):
    #     self.__class__.objects.exclude(id=self.id).delete()
    #     super(VideoLink, self).save(*args, **kwargs)

class SponsoredBlockTwo(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.FileField(upload_to='images', null=True, blank=True)
    is_verified = models.BooleanField(default=True)

    def __str__(self):
        return 'SponsoredBlockTwo #{}'.format(self.id)

    class Meta:
        verbose_name_plural="SponsoredBlockTwo"

class SponsoredBlockThree(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.FileField(upload_to='images', null=True, blank=True)
    is_verified = models.BooleanField(default=True)

    def __str__(self):
        return 'SponsoredBlockThree #{}'.format(self.id)

    class Meta:
        verbose_name_plural="SponsoredBlockThree"


class SponsoredBlockFour(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    name2 = models.CharField(max_length=255, null=True, blank=True)
    name3 = models.CharField(max_length=255, null=True, blank=True)
    image = models.FileField(upload_to='images', null=True, blank=True)
    is_verified = models.BooleanField(default=True)

    def __str__(self):
        return 'SponsoredBlockFour #{}'.format(self.id)

    class Meta:
        verbose_name_plural="SponsoredBlockFour"


class TabOne(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.FileField(upload_to='images/kelowna', blank=True, null=True, verbose_name="Image")
    video_url = models.FileField(upload_to='videos', null=True, blank=True, verbose_name="Video")
    youtube_url = models.URLField(blank=True, null=True)  # Store the YouTube URL
    content = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        # return self.title or "BTS Kelowna"
        return 'BTS Kelowna #{}'.format(self.id)
    
    class Meta:
        verbose_name_plural="BTS Kelowna"

class TabTwo(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.FileField(upload_to='images/aldergrove', blank=True, null=True, verbose_name="Image")
    video_url = models.FileField(upload_to='videos', null=True, blank=True, verbose_name="Video")
    youtube_url = models.URLField(blank=True, null=True)  # Store the YouTube URL
    content = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return self.title or "BTS Aldergrove"
        return 'BTS Aldergrove #{}'.format(self.id)

    class Meta:
        verbose_name_plural="BTS Aldergrove"

class TabThree(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.FileField(upload_to='images/mapleridge', blank=True, null=True, verbose_name="Image")
    video_url = models.FileField(upload_to='videos', null=True, blank=True, verbose_name="Video")
    youtube_url = models.URLField(blank=True, null=True)  # Store the YouTube URL
    content = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return self.title or "BTS Maple Ridge"
        return 'BTS Maple Ridge #{}'.format(self.id)

    class Meta:
        verbose_name_plural="BTS Maple Ridge"
