from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.


class Index(View):
    def get(self, request,):
        video = VideoLink.objects.all().last()
        all_video = VideoLink.objects.all()
        sponsoredblocktwo_obj = SponsoredBlockTwo.objects.filter(is_verified=True)
        sponsoredblockthree_obj = SponsoredBlockThree.objects.filter(is_verified=True)
        sponsoredblockfour_obj = SponsoredBlockFour.objects.filter(is_verified=True)
        latest_video = TabOne.objects.all().last()
        all_videos = TabOne.objects.all()
        latest_video2 = TabTwo.objects.all().last()
        all_videos2 = TabTwo.objects.all()
        all_videos3 = TabThree.objects.all()

        for videoKelowna in all_videos:
            if videoKelowna.youtube_url and '/embed/' in videoKelowna.youtube_url:
                videoKelowna.video_id = videoKelowna.youtube_url.split('/embed/')[1].split('?')[0]
            else:
                videoKelowna.video_id = None

        for videoAldergrove in all_videos2:
            if videoAldergrove.youtube_url and '/embed/' in videoAldergrove.youtube_url:
                videoAldergrove.video_id = videoAldergrove.youtube_url.split('/embed/')[1].split('?')[0]
            else:
                videoAldergrove.video_id = None

        for videoMapleRidge in all_videos3:
            if videoMapleRidge.youtube_url and '/embed/' in videoMapleRidge.youtube_url:
                videoMapleRidge.video_id = videoMapleRidge.youtube_url.split('/embed/')[1].split('?')[0]
            else:
                videoMapleRidge.video_id = None

        context = {
            'latest_video': latest_video,
            'all_videos': all_videos,
            'latest_video2': latest_video2,
            'all_videos2': all_videos2,
            'all_videos3': all_videos3,
            'all_video':all_video,
            'sponsoredblocktwo_obj':sponsoredblocktwo_obj,
            'sponsoredblockthree_obj':sponsoredblockthree_obj,
            'sponsoredblockfour_obj':sponsoredblockfour_obj,
            'signup_form': UserCreationForm(),
            'login_form': AuthenticationForm(),
            }
        return render(request,'index.html',context)

    def post(self,request):
        print(request.POST)
        data=Connect()
        data.name=request.POST.get('name')
        data.email=request.POST.get('email')
        data.number=request.POST.get('number')
        data.messages=request.POST.get('messages')
        data.save()
        messages.info(request, "Thankyou for your query, we'll get back to you soon.")
        return redirect('index')
   

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('members_home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def members_home_view(request):
    return render(request, 'web_app/members_home.html')
