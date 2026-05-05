import json
import boto3

client_bedrock_knowledgebase = boto3.client(
    'bedrock-agent-runtime',
    region_name='us-east-1'
)

def lambda_handler(event, context):
    try:
        # Handle API Gateway or direct invocation
        if 'body' in event:
            body = json.loads(event['body'])
            user_prompt = body.get('prompt', '')
        else:
            user_prompt = event.get('prompt', '')

        print("User Prompt:", user_prompt)

        response = client_bedrock_knowledgebase.retrieve_and_generate(
            input={
                'text': user_prompt
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': 'EDXMGSTEEY',
                    'modelArn': 'arn:aws:bedrock:us-east-1:463646775279:application-inference-profile/i9asueonpnr3'
                }
            }
        )

        response_text = response.get('output', {}).get('text', '')

        return {
            'statusCode': 200,
            'body': json.dumps(response_text)
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }