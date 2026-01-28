import os
from azure.storage.blob import BlobServiceClient

# Azure Setup from settings
ACCOUNT_NAME = 'promisesmovie'
ACCOUNT_KEY = 'LPv4wV1ANw45tbGVfkPtpfeUnuDabgS7GVlSe1WOW3tMKAbPqXaNAu+hMNlNGImjpMv5XH3WKbSZ+AStzpP+xw=='
CONTAINER_NAME = 'media'

def list_blobs():
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={ACCOUNT_NAME};AccountKey={ACCOUNT_KEY};EndpointSuffix=core.windows.net"
    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        
        print(f"Listing image blobs in container '{CONTAINER_NAME}':")
        blobs_list = container_client.list_blobs()
        count = 0
        image_count = 0
        for blob in blobs_list:
            if blob.name.startswith('images/') or blob.name.lower().endswith(('.jpg', '.png', '.jpeg')):
                if image_count < 20: 
                     print(f" - {blob.name}")
                image_count += 1
            count += 1
        
        print(f"\nTotal blobs processed: {count}")
        print(f"Total image blobs found: {image_count}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_blobs()
