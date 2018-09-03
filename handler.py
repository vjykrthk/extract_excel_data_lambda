import traceback

import boto3
import pandas as pd

sheet_name = 'MICs List by CC'

s3_client = boto3.client('s3')


def extract_excel_mics_list_by_cc_data(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    url = get_excel_url(bucket, key)
    json_data = get_excel_mics_list_by_cc_json(url)
    if json_data:
        upload_json_file(json_data, bucket, key)


def get_excel_url(bucket, key):
    url = s3_client.generate_presigned_url(
        'get_object', Params={'Bucket': bucket, 'Key': key})
    return url


def get_excel_mics_list_by_cc_json(url):
    try:
        df = pd.read_excel(url, sheet_name=sheet_name)
        to_json = df.to_json(orient='records')
        return to_json
    except Exception as e:
        print(traceback.format_exc())


def get_file_name(key):
    return key.split('.')[0]


def upload_json_file(data, bucket, key):
    binary_data = bytes(data, 'utf-8')
    file_name = get_file_name(key)
    s3_client.put_object(Body=binary_data, Bucket=bucket, Key='{}.json'.format(file_name))


if __name__ == '__main__':
    good_excel_event = {
        'Records': [{'s3': {'bucket': {'name': 'vjykrthk-extract-excel-data'}, 'object': {'key': 'ISO10383_MIC.xls'}}}]}
    context = {}
    extract_excel_mics_list_by_cc_data(good_excel_event, context)
