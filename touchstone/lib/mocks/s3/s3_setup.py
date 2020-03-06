import os

from minio import Minio


class S3Setup(object):
    def __init__(self, s3_client: Minio):
        self.__s3_client = s3_client

    def init(self, path: str, defaults: dict):
        for bucket in self.__s3_client.list_buckets():
            objects = self.__s3_client.list_objects(bucket.name, recursive=True)
            for m_object in objects:
                self.__s3_client.remove_object(bucket.name, m_object.object_name)
            self.__s3_client.remove_bucket(bucket.name)

        for bucket in defaults['buckets']:
            bucket_name = bucket['name']
            self.__s3_client.make_bucket(bucket_name)
            for m_object in bucket['objects']:
                object_path = os.path.join(path, m_object['path'])
                file_stat = os.stat(object_path)
                with open(object_path, 'rb') as data:
                    self.__s3_client.put_object(
                        bucket_name,
                        m_object['name'],
                        data,
                        file_stat.st_size,
                        m_object['content-type']
                    )

    def create_bucket(self, name: str):
        self.__s3_client.make_bucket(name)

    def put_object(self, bucket_name: str, object_name: str, data: bytes,
                   content_type: str = 'application/octet-stream'):
        length = os.stat(data).st_size
        self.__s3_client.put_object(bucket_name, object_name, data, length, content_type)
