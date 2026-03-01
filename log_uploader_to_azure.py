import boto3
import requests
import hashlib

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key    = event['Records'][0]['s3']['object']['key']
    obj = s3.get_object(Bucket=bucket, Key=key)
    data = obj['Body'].read()

    sha256_hash = hashlib.sha256(data).hexdigest()

    sas_url = "https://cloudtraillogsbackup.blob.core.windows.net/trailbackup"
    token = "<insert-SAS-token-here>"
    
    upload_url = f"{sas_url}/{key}?{token}"
    headers = {'x-ms-blob-type': 'BlockBlob'}
    requests.put(upload_url, headers=headers, data=data)
    
    hash_filename = key + ".hash.txt"
    hash_url = f"{sas_url}/{hash_filename}?{token}"
    requests.put(hash_url, headers=headers, data=sha256_hash.encode())

    return {'statusCode': 200}