import os
import boto3


if __name__ == '__main__':
    import sys

    bucket = sys.argv[1]
    s3 = boto3.resource('s3')

    data_dir = '/'.join(os.path.realpath(__file__).split('/')[:-2]) + '/data'
    data_dir = os.path.join(data_dir, bucket)
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)
    print 'Transferring data from', bucket, 'to', data_dir

    for obj in s3.Bucket(bucket).objects.all():
        print 'Downloading', obj.key
        s3.Bucket(bucket).download_file(obj.key, os.path.join(data_dir, obj.key))