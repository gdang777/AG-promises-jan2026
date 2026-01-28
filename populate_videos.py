import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'promises.settings')
django.setup()

from web_app.models import VideoLink

def populate_videos():
    # List of video filenames relative to the container root/upload_to path
    # Based on production inspection, they are in 'videos/' (upload_to='videos')
    # The Azure container path is likely 'media/videos/...' but the upload_to handles the subdirectory.
    # We will try to match the format that works.
    
    videos = [
        "SFU-FINAL-Video-1080p.mp4",
        "Promises_Promo_April_2025.mp4",
        "Lt_Johal_-_FINAL_540.mp4",
        "History_Informs_the_Future_SFU_Nov15_Cut_-_720p.mp4"
    ]

    print(f"Current VideoLink count: {VideoLink.objects.count()}")
    
    # Ideally, we wipe the existing one to ensure a clean slate of these 4 specific videos
    print("Clearing existing VideoLink entries...")
    VideoLink.objects.all().delete()

    for filename in videos:
        # Construct the path that fits into the FileField
        # Usually Django FileField stores the path relative to MEDIA_ROOT (or container root)
        # The model has upload_to='videos', so we expect 'videos/filename.mp4'
        
        file_path = f"videos/{filename}"
        
        # Create object
        # We manually set the video_url.name to point to the file
        vid = VideoLink()
        vid.video_url.name = file_path
        vid.save()
        
        print(f"Created VideoLink: {vid} ->Path: {vid.video_url.name}")

    print(f"New VideoLink count: {VideoLink.objects.count()}")

if __name__ == '__main__':
    populate_videos()
