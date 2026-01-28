import os
from azure.storage.blob import BlobServiceClient, ContentSettings

# Azure Settings
ACCOUNT_NAME = 'promisesmovie'
ACCOUNT_KEY = 'LPv4wV1ANw45tbGVfkPtpfeUnuDabgS7GVlSe1WOW3tMKAbPqXaNAu+hMNlNGImjpMv5XH3WKbSZ+AStzpP+xw=='
CONTAINER_NAME = 'media'

# Local Media Root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

def upload_files():
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={ACCOUNT_NAME};AccountKey={ACCOUNT_KEY};EndpointSuffix=core.windows.net"
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)

        print(f"Starting upload from {MEDIA_ROOT} to container '{CONTAINER_NAME}'...")

        walk_dir = MEDIA_ROOT
        for root, dirs, files in os.walk(walk_dir):
            for filename in files:
                # Construct local file path
                local_path = os.path.join(root, filename)
                
                # Construct blob name (relative path from media root)
                # e.g. /path/to/media/images/file.png -> images/file.png
                relative_path = os.path.relpath(local_path, MEDIA_ROOT)
                blob_name = relative_path

                # Skip hidden files
                if filename.startswith('.'):
                    continue

                print(f"Uploading {blob_name}...")
                
                # Determine content type (basic check)
                content_type = 'application/octet-stream'
                if filename.lower().endswith('.png'):
                    content_type = 'image/png'
                elif filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                    content_type = 'image/jpeg'
                elif filename.lower().endswith('.mp4'):
                    content_type = 'video/mp4'

                content_settings = ContentSettings(content_type=content_type)

                with open(local_path, "rb") as data:
                    container_client.upload_blob(name=blob_name, data=data, overwrite=True, content_settings=content_settings)
        
        print("\nUpload complete!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    upload_files()
