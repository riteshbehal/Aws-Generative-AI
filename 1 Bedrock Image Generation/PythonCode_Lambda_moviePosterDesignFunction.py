import json
import boto3
import base64
from datetime import datetime

bedrock_client = boto3.client("bedrock-runtime")
s3_client = boto3.client("s3")

BUCKET_NAME = "amzn-web-infrat2"
MODEL_ID = "stability.sd3-5-large-v1:0"


def lambda_handler(event, context):
    try:
        prompt = event.get("prompt", "A dog near the sea at sunset")

        request_body = {
            "prompt": prompt,
            "seed": 0,
            "output_format": "png",
            "aspect_ratio": "1:1"
        }

        response = bedrock_client.invoke_model(
            modelId=MODEL_ID,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(request_body)
        )

        response_body = json.loads(response["body"].read())

        if "images" not in response_body or not response_body["images"]:
            raise ValueError("No image returned from model")

        image_base64 = response_body["images"][0]
        image_bytes = base64.b64decode(image_base64)

        file_name = f"poster-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}.png"

        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=image_bytes,
            ContentType="image/png"
        )

        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": file_name},
            ExpiresIn=3600
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "image_url": presigned_url
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }