import boto3
import os
import logging
import json
from datetime import datetime 

# Configure structured logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Connect to dynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['AppointmentsTable'])

def generate_appointment_id():
    """
    Generates a unique appointment ID using the current timestamp.

    returns:
        str: Unique appointment ID
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"APT-{timestamp}"

def save_appointment(data):
    """
    Saves appointment data to dynamoDB.

    args:
        data (dict): appointment information

    returns:
        dict: DynamoDB response
    """
    response = table.put_item(Item=data)
    return response


def lambda_handler(event, context):
    """
    Lambda function handler for appointment operations.
    Routes based on HTTP method with error handling and structured logging.
    """
    try:   
        logger.info("Received POST request", extra={
            'path': event.get('path'),
            'request_id': context.aws_request_id
        })
        
        # POST - Create appointment
        body = json.loads(event['body'])
        appointment_data = {
            "appointment_id": generate_appointment_id(),
            "patient_name": body['patient_name'],
            "doctor_name": body['doctor_name'],
            "appointment_date": body['appointment_date'],
            "appointment_time": body['appointment_time'],
            "state": "pending"
        }
            
        save_appointment(appointment_data)
        logger.info("Appointment created successfully", extra={
            'appointment_id': appointment_data['appointment_id']
        })
            
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Appointment created successfully',
                'appointment_id': appointment_data['appointment_id']
            })
        }
    
    except json.JSONDecodeError:
        logger.error("Invalid JSON body")
        return {'statusCode': 400, 'body': json.dumps({'message': 'Invalid JSON body'})}

    except KeyError as e:
        logger.error("Missing required field", extra={'error': str(e)})
        return {
            'statusCode': 400,
            'body': json.dumps({'message': f'Missing required field: {str(e)}'})
        }
    
    except Exception as e:
        logger.error("Unexpected error", extra={'error': str(e)}, exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error'})}