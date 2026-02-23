import boto3
import json
from datetime import datetime 

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
    Retrives an appoiontment by ID from DynamoDB.

    args:
        appointment_id (str): unique appointment identifier

    returns:
        dict: appointment data or none if not found
    """
    response = table.get_item(Key={'appointment_id': appointment_id})
    return response.get('Item', None)

def lambda_handler(event, context):
    """
    Lambda function handler for appointment operations.
    Routes based on HTTP method.
    """
    http_method = event['httpMethod']

    # POST - create appointment
    if http_method == 'POST':
        body = json.loads(event['body'])
        appointment_data = {
            "appointment_id": generate_appointment_id(),
            "patient_name": body["patient_name"],
            "doctor_name": body["doctor_name"],
            "appointment_date": body["appointment_date"],
            "appointment_time": body["appointment_time"],
            "state": "pending"
        }

        save_appointment(appointment_data)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Appointment created successfully',
                'appointment_id': appointment_data['appointment_id']
            })
        }
    
    # GET - retrieve appointment
    elif http_method == 'GET':
        appointment_id = event['pathParameters']['id']
        appointment = get_appointment(appointment_id)

        if appointment:
            return {
                'statusCode': 200,
                'body': json.dumps(appointment)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Appointment not found'})
            }