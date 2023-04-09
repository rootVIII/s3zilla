# MIT License Copyright (c) 2019-2023 rootVIII
from boto3.session import Session


class S3:
    def __init__(self):
        self.session = Session()


class S3Session(S3):
    def __init__(self):
        S3.__init__(self)
        self.session_client = self.session.client('s3')

    def upload_s3(self, file_path: str, bucket: str, bucket_path: str):
        with open(file_path, 'rb') as file_handle:
            self.session_client.upload_fileobj(file_handle, bucket, bucket_path)

    def download_s3(self, bucket: str, remote_file_path: str, local_file_name: str):
        self.session_client.download_file(bucket, remote_file_path, local_file_name)

    def list_avail_buckets(self) -> list:
        return [bucket['Name'] for bucket in self.session_client.list_buckets()['Buckets']]

    def delete_obj(self, bucket, bucket_path: str):
        _ = [self.session_client.delete_object(Bucket=bucket, Key=obj['Key'])
             for obj in self.session_client.list_objects_v2(Bucket=bucket,
                                                            Prefix=bucket_path)['Contents']]


class S3Resource(S3):
    def __init__(self):
        S3.__init__(self)
        self.resource_client = self.session.resource('s3')

    def list_bucket_contents(self, bucket: str) -> list:
        bucket = self.resource_client.Bucket(bucket)
        return [summary.key for summary in bucket.objects.filter()]


class S3Client(S3Session, S3Resource):
    def __init__(self):
        S3Session.__init__(self)
        S3Resource.__init__(self)
