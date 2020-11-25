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
    table = DYNDBRES.Table("iccdf-4byte-data-room-v1-user-dev")

    array_body = {
        "tableName": "iccdf-4byte-data-room-v1-user-dev",
        "tableIdKey": "username",
        "activity_id": str(secrets.token_hex(64)),
        "event_operation": "CREATE",
        "last_modified_date": str(datetime.datetime.now()),
        "hash": str(secrets.token_hex(64))
    }
    body.update(array_body)

    json_object = json.dumps(body, indent=4)
    LOGGER.info("Final Transformed Payload")
    LOGGER.info(json_object)

    # call arn:aws:lambda:us-west-2:519352267686:function:iccdf_generic_write_to_db
    # msg = {"key":"new_invocation", "at": datetime.now()}
    # invoke_response = lambda_client.invoke(FunctionName="iccdf_generic_write_to_db",
    #                                         InvocationType='Event',
    #                                       Payload=json_object2)

    response = table.put_item(Item=body)
    LOGGER.info(response)

    return {
        'status_code': response.get("ResponseMetadata").get("HTTPStatusCode"),
        'body': json_object,
        'db_flag': 0,
        'message': 'Data successfully updated in user table'
    }
