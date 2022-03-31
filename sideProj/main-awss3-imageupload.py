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


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


#url = create_presigned_url('BUCKET_NAME', 'OBJECT_NAME')
bucket_name = 'jongsul'
filename = 'samplepng.jpg'


if __name__ == '__main__':
    import time
    # current working directory
    print(os.path.dirname(os.path.abspath(__file__)))
    print()
    # env variable setting
    os.environ['AWS_SHARED_CREDENTIALS_FILE'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "awsconfig.ini")

    s0 = time.time()
    # upload local file to S3 bucket
    if upload_file(filename, bucket_name):
        print("upload success.")
        s1 = time.time()
        # create url
        url = create_presigned_url(bucket_name, filename)
        print(f"filename: {filename}")
        print(f"Your url: {url}")
    else:
        print("upload denied.")
    s2 = time.time()
    print(f'total time: {s2 - s0}')
    print(f'upload time: {s1 - s0}')
    print(f'url creation time: {s2 - s1}')