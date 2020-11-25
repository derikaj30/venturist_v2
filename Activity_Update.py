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
    table = DYNDBRES.Table("iccdf-4byte-data-room-v1-activity-dev")

    response = table.update_item(
        Key={
            'activity_id': body.get("activity_id")
        },
        UpdateExpression="SET activity_name = :activity_name, last_modified_date = :last_modified_date, "
                         "activity_action = :activity_action, activity_user = :activity_user, activity_subroom = "
                         ":activity_subroom, activity_when = :activity_when, event_operation = :event_operation ",
        ExpressionAttributeValues={
            ':activity_name': str(body.get("activity_name")),
            ':last_modified_date': str(datetime.datetime.now()),
            ':activity_action': str(body.get("activity_action")),
            ':activity_user': str(body.get("activity_user")),
            ':activity_subroom': str(body.get("activity_subroom")),
            ':activity_when': str(body.get("activity_when")),
            ':event_operation': "UPDATE"
        }
    )
    LOGGER.info(response)

    return {
        'status_code': response.get("ResponseMetadata").get("HTTPStatusCode"),
        'body': response,
        'db_flag': 0,
        'message': 'Data successfully updated in activity table'
    }
