import boto3
import os
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['AppointmentsTable'])

def lambda_handler(event, context):
    try:
        appointment_id = event['pathParameters']['id']
        logger.info("Request received", extra={
            'appointment_id': appointment_id
        })

        # Delete the appointment from DynamoDB
        response = table.delete_item(
            Key={'appointment_id': appointment_id},
            ConditionExpression="attribute_exists(appointment_id)"
        )

        logger.info("Appointment deleted successfully", extra={
            'appointment_id': appointment_id
        })
        return {'statusCode': 200, 'body': json.dumps({'message': 'Appointment deleted successfully'})}
        
    except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
        logger.warning("Appointment not found", extra={'appointment_id': appointment_id})
        return {'statusCode': 404, 'body': json.dumps({'message': 'Appointment not found'})}  
    except KeyError as e:
        logger.error("Missing path parameter", extra={'error': str(e)})
        return {'statusCode': 400, 'body': json.dumps({'message': 'Missing path parameter: id'})}    
    except Exception as e:
        logger.error("Error deleting appointment", exc_info=True, extra={
            'error_message': str(e)
        })
        return {'statusCode': 500, 'body': json.dumps({'message': 'Internal server error'})}