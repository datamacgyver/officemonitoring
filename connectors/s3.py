from datetime import datetime
import logging
import boto3
from botocore.exceptions import ClientError
from secure.logons import s3_bucket, s3_key, s3_secret


CLIENT = boto3.client(
    's3',
    aws_access_key_id=s3_key,
    aws_secret_access_key=s3_secret
)


def get_time():
    return str(datetime.strftime(datetime.now(), '%Y%m%dT%H%M%S'))


def _upload_file(file_name, bucket, object_name=None):
    """Upload a given file to S3"""
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    try:
        _ = CLIENT.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# TODO: Actually make a temporary file! Scratch that, write string directly to S3
def _make_temp(a_dict, f_name='temp.json'):
    a_dict = str(a_dict)
    with open(f_name, 'w') as f:
        f.write(a_dict)

    return f_name


def push_new_reading(val, table, col=None):
    """Push a reading to S3, for example the shed temperature"""
    col = col if col else table
    val = str(val)
    time = get_time()

    out_dict = {'timestamp': time, 'variable': col, 'value': val}

    f = _make_temp(out_dict)
    _upload_file(f, s3_bucket, object_name='%s/%s.json' % (table, time))


def record_hive_command(hive_command):
    """Record a hive action on S3, for example turning the heating on"""
    time = get_time()
    out_dict = {'timestamp': time, ' hive_command':  hive_command}

    f = _make_temp(out_dict)
    _upload_file(f, s3_bucket, object_name='hivecommands/%s.json' % time)


if __name__ == "__main__":
    push_new_reading(0, 'stub')
