# import necessary libraries
import boto3
import datetime
import json
import logging
import secrets

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
    table = DYNDBRES.Table("iccdf-4byte-data-room-v1-photo-dev")

    response = table.update_item(
        Key={
            'client_id': body.get("client_id")
        },
        UpdateExpression="SET dataroom_name = :dataroom_name, event_operation = :event_operation, "
                         "last_modified_date = :last_modified_date, dataroom_shareData = :dataroom_shareData,  "
                         "dataroom_tier = :dataroom_tier, photolocation = :photolocation",
        ExpressionAttributeValues={
            ':dataroom_name': str(body.get("dataroom_name")), ':event_operation': "UPDATE",
            ':last_modified_date': str(datetime.datetime.now()), ':photolocation': str(body.get("photolocation")),
            ':dataroom_shareData': str(body.get("dataroom_shareData")), ':dataroom_tier': str(body.get("dataroom_tier"))
        }
    )
    LOGGER.info(response)

    return {
        'status_code': response.get("ResponseMetadata").get("HTTPStatusCode"),
        'body': response,
        'db_flag': 0,
        'message': 'Data successfully updated in dataroom table'
    }
