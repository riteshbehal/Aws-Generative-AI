import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):

    print("Event:", event)

    # 🔹 Extract AccountId safely
    account_id = None
    for param in event.get('parameters', []):
        if param.get('name') == 'AccountId':
            account_id = param.get('value')

    if account_id is None:
        return build_response(event, 400, {"error": "Missing AccountId"})

    # 🔹 Validate AccountId is numeric
    try:
        account_id = int(account_id)
    except:
        return build_response(event, 400, {"error": "AccountId must be a number"})

    # 🔹 Fetch from DynamoDB
    try:
        response = client.get_item(
            TableName='AccountStatus',
            Key={'AccountId': {'N': str(account_id)}}
        )
    except Exception as e:
        return build_response(event, 500, {"error": f"DynamoDB error: {str(e)}"})

    print("DynamoDB response:", response)

    item = response.get('Item')

    if not item:
        return build_response(event, 404, {"error": "Account not found"})

    # 🔹 Safely extract values
    account_data = {
        "AccountId": int(item.get('AccountId', {}).get('N', 0)),
        "AccountName": item.get('AccountName', {}).get('S', 'N/A'),
        "AccountStatus": item.get('AccountStatus', {}).get('S', 'N/A'),
        "Reason": item.get('Reason', {}).get('S', 'N/A')
    }

    return build_response(event, 200, account_data)


# 🔹 Standard Bedrock response builder
def build_response(event, status_code, body):
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": event.get("actionGroup") or "AccountStatusAction",
            "apiPath": event.get("apiPath") or "/newBankAccountStatus",
            "httpMethod": event.get("httpMethod") or "GET",
            "httpStatusCode": status_code,
            "responseBody": {
                "application/json": body   # ⚠️ Do NOT use json.dumps
            }
        },
        "sessionAttributes": event.get("sessionAttributes", {}),
        "promptSessionAttributes": event.get("promptSessionAttributes", {})
    }