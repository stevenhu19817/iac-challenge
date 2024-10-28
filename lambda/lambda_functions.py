import json
import os
import boto3

# 創建 SQS Client，用於發送和接收消息
sqs = boto3.client("sqs")
# 從環境變數中獲取 SQS 佇列的 URL
QUEUE_URL = os.environ["QUEUE_URL"]


# 定義處理 POST 請求的 Lambda 函數
def post_handler(event, context):
    try:
        body = json.loads(event["body"])
        sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=json.dumps(body))
        return {
            "statusCode": 200,
            "body": json.dumps("Message sent to SQS successfully"),
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(f"Error: {str(e)}")}


# 定義處理 GET 請求的 Lambda 函數
def get_handler(event, context):
    try:
        response = sqs.receive_message(QueueUrl=QUEUE_URL, MaxNumberOfMessages=1)
        if "Messages" in response:
            message = response["Messages"][0]
            sqs.delete_message(
                QueueUrl=QUEUE_URL, ReceiptHandle=message["ReceiptHandle"]
            )
            return {"statusCode": 200, "body": message["Body"]}
        else:
            return {"statusCode": 404, "body": json.dumps("No messages in queue")}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(f"Error: {str(e)}")}
