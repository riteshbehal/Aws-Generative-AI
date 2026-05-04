import json
import boto3

client_bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def lambda_handler(event, context):
    try:
        print("EVENT:", event)

        # ✅ Handle BOTH formats
        if 'body' in event:
            body = json.loads(event['body'])
            user_prompt = body.get('prompt', '')
        else:
            user_prompt = event.get('prompt', '')

        if not user_prompt:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Prompt is required"})
            }

        response = client_bedrock.invoke_model(
            modelId='amazon.nova-pro-v1:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"text": user_prompt}
                        ]
                    }
                ],
                "inferenceConfig": {
                    "temperature": 0.7,
                    "topP": 0.9,
                    "maxTokens": 200
                }
            })
        )

        response_body = json.loads(response['body'].read())
        output_text = response_body['output']['message']['content'][0]['text']

        return {
            "statusCode": 200,
            "body": json.dumps({"response": output_text})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
