import boto3
import logging
import json
from datetime import datetime 

# Configure structured logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Connect to dynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('AppointmentsTable')


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

def update_appointment_state(appointment_id, new_state):
    """
    Updates the state of an existing appointment.

    args:
       appointment_id (str): unique appointment identifier
       new_state (str): new state value (pending/confirmed/cancelled) 

    returns:
        dict: DynamoDB response
    """
    response = table.update_item(
        Key={'appointment_id': appointment_id},
        UpdateExpression="SET #s = :new_state",
        ExpressionAttributeNames={'#s': 'state'},
        ExpressionAttributeValues={':new_state': new_state},
    )
    return response

def delete_appointment(appointment_id):
    """
    Deletes an appointment from DynamoDB.

    args:
        appointment_id (str): Unique appointment identifier

    returns:
        dict: DynamoDB response
    """
    response = table.delete_item(Key={'appointment_id': appointment_id})
    return response

def lambda_handler(event, context):
    """
    Lambda function handler for appointment operations.
    Routes based on HTTP method with error handling and structured logging.
    """
    try:
        http_method = event['httpMethod']
        logger.info(f"Received {http_method} request", extra={
            'method': http_method,
            'path': event.get('path'),
            'request_id': context.request_id
        })
        
        # POST - Create appointment
        if http_method == 'POST':
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
        
        # GET - Retrieve appointment
        elif http_method == 'GET':
            appointment_id = event['pathParameters']['id']
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
        
        # PUT - Update appointment state
        elif http_method == 'PUT':
            appointment_id = event['pathParameters']['id']
            body = json.loads(event['body'])
            new_state = body['state']
            
            update_appointment_state(appointment_id, new_state)
            logger.info("Appointment updated", extra={
                'appointment_id': appointment_id,
                'new_state': new_state
            })
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Appointment state updated successfully',
                    'appointment_id': appointment_id,
                    'new_state': new_state
                })
            }
        
        # DELETE - Remove appointment
        elif http_method == 'DELETE':
            appointment_id = event['pathParameters']['id']
            
            delete_appointment(appointment_id)
            logger.info("Appointment deleted", extra={'appointment_id': appointment_id})
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Appointment deleted successfully',
                    'appointment_id': appointment_id
                })
            }
        
        # Method not supported
        else:
            logger.warning("Method not allowed", extra={'method': http_method})
            return {
                'statusCode': 405,
                'body': json.dumps({'message': 'Method not allowed'})
            }
    
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
            'body': json.dumps({'message': 'Internal server error'})
        }