import boto3
import os
import json
import logging  
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['AppointmentsTable'])

def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")

def lambda_handler(event, context):
    try:
        appointment_id = event['pathParameters']['id']
        logger.info("Request received", extra={
            'appointment_id': appointment_id
        })

        # Fetch the appointment from DynamoDB
        response = table.get_item(Key={'appointment_id': appointment_id})
        appointment = response.get('Item')

        if not appointment:
            logger.warning("Appointment not found", extra={
                'appointment_id': appointment_id
            })
            return {'statusCode': 404, 'body': json.dumps({'message': 'Appointment not found'})}

        logger.info("Appointment retrieved successfully", extra={
            'appointment_id': appointment_id,
            'appointment_data': appointment
        })

        return {
            'statusCode': 200, 
            'body': json.dumps(appointment, default=decimal_serializer)
        }    
    except KeyError as e:
        logger.error("Missing path parameter", extra={'error': str(e)})
        return {'statusCode': 400, 'body': json.dumps({'message': 'Missing path parameter: id'})}    
    except Exception as e:
        logger.error("Error retrieving appointment", exc_info=True, extra={
            'error_message': str(e)
        })
        return {'statusCode': 500, 'body': json.dumps({'message': 'Internal server error'})}

