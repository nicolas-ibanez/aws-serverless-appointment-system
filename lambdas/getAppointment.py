import boto3
import json
import logging

def get_appointment(appointment_id):
    """
    Retrives an appointment by ID from DynamoDB.

    args:
        appointment_id (str): unique appointment identifier

    returns:
        dict: appointment data or none if not found
    """
    response = table.get_item(Key={'appointment_id': appointment_id})
    return response.get('Item', None)

def lambda_handler(event, context):
    try:
        appointment_id = event['pathParameters']['id']
        body = json.loads(event['body'])
        logger.info("Retrieving appointment", extra={'appointment_id': appointment_id})

        appointment = get_appointment(appointment_id)
            
        if appointment:
            return {
                'statusCode': 200,
                'body': json.dumps(appointment)
            }
        else:
            logger.warning("Appointment not found", extra={'appointment_id': appointment_id})
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Appointment not found'})
            }