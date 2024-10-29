from celery import shared_task
from bucket import bucket


# TODO:Can be async javascript?
def list_objects_task():
    result = bucket.list_objects()
    return result


@shared_task
def delete_object_task(key):
    result = bucket.delete_object(key)
    return result


@shared_task
def download_object_task(key):
    result = bucket.download_object(key)
    return result