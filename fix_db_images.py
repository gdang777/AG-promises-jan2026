import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'promises.settings')
django.setup()

from web_app.models import TabOne, TabTwo, TabThree, SponsoredBlockTwo, SponsoredBlockThree, SponsoredBlockFour, VideoLink

# Map of Models to their image fields
MODELS_TO_FIX = [
    (TabOne, 'image_url'),
    (TabTwo, 'image_url'),
    (TabThree, 'image_url'),
    (SponsoredBlockTwo, 'image'),
    (SponsoredBlockThree, 'image'),
    (SponsoredBlockFour, 'image'),
    (VideoLink, 'background_url')
]

# Get list of actual available files in local media
MEDIA_ROOT = settings.MEDIA_ROOT
AVAILABLE_FILES = []
for root, dirs, files in os.walk(MEDIA_ROOT):
    for filename in files:
        # Rel path from MEDIA_ROOT
        full_path = os.path.join(root, filename)
        rel_path = os.path.relpath(full_path, MEDIA_ROOT)
        AVAILABLE_FILES.append(rel_path)

print(f"Index of {len(AVAILABLE_FILES)} available media files created.")

def find_best_match(current_path):
    if not current_path:
        return None
    
    # direct match?
    if current_path in AVAILABLE_FILES:
        return current_path
        
    # try removing suffix (assumes format name_SUFFIX.ext)
    basename = os.path.basename(current_path)
    dirname = os.path.dirname(current_path)
    
    name, ext = os.path.splitext(basename)
    
    # Heuristic: split by underscore and remove last part if it looks like a hash
    # e.g. IMG_7604-R1_VtIKjcf -> IMG_7604-R1
    if '_' in name:
        parts = name.rsplit('_', 1)
        candidate_name = parts[0] + ext
        candidate_path = os.path.join(dirname, candidate_name)
        
        # Check if candidate exists
        for f in AVAILABLE_FILES:
            if f == candidate_path:
                return f
            if f.lower() == candidate_path.lower(): # Case insensitive check
                return f
            
    # Try finding any file that starts with the main part of the name
    # e.g. "IMG_7604"
    search_prefix = parts[0] if '_' in name else name
    for f in AVAILABLE_FILES:
        # Check if file is in the same directory
        if os.path.dirname(f) == dirname:
             f_name = os.path.basename(f)
             if f_name.startswith(search_prefix):
                 return f
                 
    return None

def fix_records():
    for model_class, field_name in MODELS_TO_FIX:
        print(f"Checking {model_class.__name__}...")
        count = 0
        updated = 0
        
        for obj in model_class.objects.all():
            current_val = getattr(obj, field_name)
            if not current_val:
                continue
                
            current_path = str(current_val)
            
            # Check if it exists
            if current_path in AVAILABLE_FILES:
                continue
                
            # Find match
            new_path = find_best_match(current_path)
            
            if new_path:
                print(f"  Fixing {obj}: {current_path} -> {new_path}")
                setattr(obj, field_name, new_path)
                obj.save()
                updated += 1
            else:
                print(f"  Could not find match for: {current_path}")
                
        print(f"  Updated {updated} records.")

if __name__ == "__main__":
    fix_records()
