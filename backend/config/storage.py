from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StorageBase(S3Boto3Storage):
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN


class StaticStorage(StorageBase):
    location = "static"
    default_acl = "public-read"
    file_overwrite = True
    querystring_auth = False
    secure_urls = False


class MediaStorage(StorageBase):
    location = "media"
    default_acl = "public-read"
    file_overwrite = False
    querystring_auth = False
    secure_urls = False


class LogsStorage(StorageBase):
    bucket_name = settings.AWS_LOGS_BUCKET_NAME
    location = ""
    default_acl = "private"
    file_overwrite = True
    querystring_auth = True
    secure_urls = False
