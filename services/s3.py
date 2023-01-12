import boto3
from botocore.exceptions import ClientError
from decouple import config
from werkzeug.exceptions import InternalServerError


class S3Service:
    def __init__(self):
        key = config('AWS_ACCESS_KEY')
        secret_key = config('AWS_SECRET_KEY')
        self.bucket_name = config('AWS_BUCKET_NAME')
        self.region = config('AWS_REGION')
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=key,
            aws_secret_access_key=secret_key,
            region_name=self.region
        )

    def upload(self, file_name, key):
        try:
            self.s3.upload_file(file_name, self.bucket_name, key)
            return f'https://{self.bucket_name}.s3.amazonaws.com/{key}'
        except ClientError:
            raise InternalServerError


    def remove(self, key):
        try:
            response = self.s3.delete_object(
                Bucket=self.bucket_name,
                Key=key,
                # MFA='string',
                # VersionId='string',
                # RequestPayer='requester',
                # BypassGovernanceRetention=True | False,
                # ExpectedBucketOwner='string'
            )
        except ClientError:
            raise InternalServerError


s3 = S3Service()


