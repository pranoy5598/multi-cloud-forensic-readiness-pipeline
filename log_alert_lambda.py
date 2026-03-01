import boto3
import gzip
import json

sns = boto3.client('sns')
TOPIC_ARN = "arn:aws:sns:eu-north-1:605926690921:suspicious-events-alerts"

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key    = event['Records'][0]['s3']['object']['key']
    
    if not key.endswith(".json.gz"):
        return {"statusCode": 200, "body": "Not a log file."}

    obj = s3.get_object(Bucket=bucket, Key=key)
    body = gzip.decompress(obj['Body'].read()).decode('utf-8')
    logs = json.loads(body)

    for record in logs.get('Records', []):
        if record.get("eventName") in ["DeleteTrail", "StopLogging", "CreateUser", "PutBucketPolicy"]:
            ip = record.get("sourceIPAddress")
            msg = f"Suspicious activity detected:\nEvent: {record['eventName']}\nIP: {ip}\nTime: {record['eventTime']}"
            sns.publish(TopicArn=TOPIC_ARN, Message=msg)

    return {"statusCode": 200}