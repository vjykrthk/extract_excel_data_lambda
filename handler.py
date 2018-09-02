import boto3
import pandas as pd

s3_client = boto3.client('s3')


def extract_excel_mics_list_by_cc_data(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    url = get_excel_url(bucket, key)
    json_data = get_excel_mics_list_by_cc_json(url)
    upload_json_file(json_data, bucket, key)


def get_excel_url(bucket, key):
    url = s3_client.generate_presigned_url(
        'get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=86400)
    return url


def get_excel_mics_list_by_cc_json(url):
    df = pd.read_excel(url, sheet_name='MICs List by CC')
    to_json = df.to_json(path_or_buf='test.json', orient='records')
    return to_json


def get_file_name(key):
    return key.split('.')[0]


def upload_json_file(data, bucket, key):
    binary_data = bytes(data, 'utf-8')
    file_name = get_file_name(key)
    s3_client.put_object(Body=binary_data, Bucket=bucket, Key='{}.json'.format(file_name))


if __name__ == '__main__':
    event = {'Records': [{'eventVersion': '2.0', 'eventSource': 'aws:s3', 'awsRegion': 'ap-south-1',
                          'eventTime': '2018-09-02T19:48:18.310Z', 'eventName': 'ObjectCreated:Put',
                          'userIdentity': {'principalId': 'A2RE0PJOQ3RLKS'},
                          'requestParameters': {'sourceIPAddress': '223.226.67.234'},
                          'responseElements': {'x-amz-request-id': '6F74310B3013CD1D',
                                               'x-amz-id-2': 'DcWNAeyYbWVNvpLkbnpvv8uthDHkW7XlMCbDkIeFcYzviLcLcqIpOlf59LgpqYoNdpSHkpGegY8='},
                          's3': {'s3SchemaVersion': '1.0', 'configurationId': '6860fbff-b4d2-4684-840b-0a51c60145b7',
                                 'bucket': {'name': 'vjykrthk-extract-excel-data',
                                            'ownerIdentity': {'principalId': 'A2RE0PJOQ3RLKS'},
                                            'arn': 'arn:aws:s3:::vjykrthk-extract-excel-data'},
                                 'object': {'key': 'ISO10383_MIC.xls', 'size': 1405952,
                                            'eTag': 'f2099204c3626d6158cc677875c5fd35',
                                            'sequencer': '005B8C3E823CD9E7D9'}}}]}
    context = {}
    extract_excel_mics_list_by_cc_data(event, context)
