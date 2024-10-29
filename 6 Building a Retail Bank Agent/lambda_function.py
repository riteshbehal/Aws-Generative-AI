import json
#1 Import boto3 and create client connection with DynamoDB - Link to documentation - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/get_item.html
import boto3
client=boto3.client('dynamodb')

def lambda_handler(event, context):
#2 Print event value and store the event details in a variable 
    print(f"This is the input from agent{event}")
    account_id=event['parameters'][0]['value']
#3 Create a request syntax to retrieve data from the DynamoDB Table using GET Item method - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/get_item.html
    response = client.get_item(
        TableName='customerAccountStatus',
        Key={'AccountID':{'N': account_id}})
#4 Store and print the response 
    print(response)
#5 Format the response as per the requirement of Bedrock Agent Action Group - https://docs.aws.amazon.com/bedrock/latest/userguide/agents-lambda.html
    response_body = {
        'application/json': {
            'body': json.dumps(response)
        }
    }
    
    action_response = {
        'actionGroup': event['actionGroup'],
        'apiPath': event['apiPath'],
        'httpMethod': event['httpMethod'],
        'httpStatusCode': 200,
        'responseBody': response_body
    }
    
    session_attributes = event['sessionAttributes']
    prompt_session_attributes = event['promptSessionAttributes']
    
    api_response = {
        'messageVersion': '1.0', 
        'response': action_response,
        'sessionAttributes': session_attributes,
        'promptSessionAttributes': prompt_session_attributes
    }
        
    return api_response

#6 Print the final response
    # TODO implement
