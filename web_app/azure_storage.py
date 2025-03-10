# myapp/azure_storage.py
from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'promisesmovie'
    account_key = 'LPv4wV1ANw45tbGVfkPtpfeUnuDabgS7GVlSe1WOW3tMKAbPqXaNAu+hMNlNGImjpMv5XH3WKbSZ+AStzpP+xw=='
    azure_container = 'media'
    expiration_secs = None  # Set to None for public files