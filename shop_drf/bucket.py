import boto3
from django.conf import settings
from rest_framework.response import Response

aws = settings.STORAGES['default']['OPTIONS']


class Bucket:

    def __init__(self):
        session = boto3.session.Session()
        self.conn = session.client(
            service_name='s3',
            endpoint_url=aws['endpoint_url'],
            aws_access_key_id=aws['access_key'],
            aws_secret_access_key=aws['secret_key'],

        )

    def list_objects(self):
        result = self.conn.list_objects_v2(Bucket=aws['bucket_name'])
        if result['KeyCount']:
            return result['Contents']
        return None

    def delete_object(self,key):
        is_exist = self.existing_object(key)
        if is_exist:
            self.conn.delete_object(Bucket=aws['bucket_name'],Key=key)
            return True
        else:
            return None

    def download_object(self,key):
        is_exist = self.existing_object(key)
        if is_exist:
            with open(settings.AWS_LOCAL_STORAGE + key,'wb') as f :
                self.conn.download_fileobj(aws['bucket_name'],key,f)
            return True
        else:
            return None

    def existing_object(self,key):
        try:
            self.conn.head_object(Bucket=aws['bucket_name'],Key=key)
            return True
        except self.conn.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False


bucket = Bucket()
