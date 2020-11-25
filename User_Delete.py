# import necessary libraries
import boto3
import datetime
import json
import logging

s3_client = boto3.client('s3')
dynamodb = boto3.client('dynamodb')
DYNDBRES = boto3.resource('dynamodb')

# Handler definition to read json from s3 and write to dynamo db
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def lambda_handler(event, context):
    LOGGER.info("Received event: " + json.dumps(event, indent=2))
    body = json.loads(event["body"])
    LOGGER.info("Received Request")
    LOGGER.info(body)

    # Define Dynamo table instance
    table = DYNDBRES.Table("iccdf-4byte-data-room-v1-user-dev")

    response = table.update_item(
        Key={
            'dataroom_username': body.get("dataroom_username")
        },
        UpdateExpression="SET user_disabled = :user_disabled, last_modified_date = :last_modified_date",
        ExpressionAttributeValues={
            ':user_disabled': "Yes",
            ':last_modified_date': str(datetime.datetime.now())
        }
    )
    LOGGER.info(response)

    return {
        'status_code': response.get("ResponseMetadata").get("HTTPStatusCode"),
        'body': response,
        'db_flag': 0,
        'message': 'Username is successfully disabled'
    }
