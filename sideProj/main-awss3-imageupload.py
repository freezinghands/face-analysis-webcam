import os
import boto3
import requests
from botocore.exceptions import ClientError


def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


#url = create_presigned_url('BUCKET_NAME', 'OBJECT_NAME')
bucket_name = 'jongsul'
filename = 'face-20220313-000128.jpg'


if __name__ == '__main__':
    # setup(settings)
    print(os.path.dirname(os.path.abspath(__file__)))
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = os.path.dirname(os.path.abspath(__file__)) + "\\awsconfig.ini"
    
    # execute
    url = create_presigned_url(bucket_name, filename)
    print(f"filename: {filename}")
    print(f"Your url: {url}")