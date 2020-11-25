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
        UpdateExpression="SET addedby = :addedby, event_operation = :event_operation, "
                         "last_modified_date = :last_modified_date, client_id = :client_id,  "
                         "dataroom_address = :dataroom_address, dataroom_name = :dataroom_name, eventname = "
                         ":eventname, expiredate = :expiredate, isPrivate = :isPrivate, phonenumber = :phonenumber",
        ExpressionAttributeValues={
            ':addedby': str(body.get("addedby")), ':event_operation': "UPDATE",
            ':last_modified_date': str(datetime.datetime.now()), ':client_id': str(body.get("client_id")),
            ':dataroom_address': str(body.get("dataroom_address")),
            ':dataroom_name': str(body.get("dataroom_name")), ':eventname': str(body.get("eventname")),
            ':expiredate': str(body.get("expiredate")), ':isPrivate': str(body.get("isPrivate")),
            ':phonenumber': str(body.get("phonenumber"))
        }
    )
    LOGGER.info(response)

    return {
        'status_code': response.get("ResponseMetadata").get("HTTPStatusCode"),
        'body': response,
        'db_flag': 0,
        'message': 'Data successfully updated in user table'
    }
