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

def lambda_handler(event, context):
    """
    Lambda function handler for creating appointments.
    """
    # Parse the incoming event data
    body = json.loads(event['body'])

    # Generate appointment data with generated ID
    appointment_data = {
        "appointment_id": generate_appointment_id(),
        "patient_name": body['patient_name'],
        "doctor_name": body['doctor_name'],
        "appointment_date": body['appointment_date'],
        "appointment_time": body['appointment_time'],
        "state": "pending"  # Default state
    }

    # Save the appointment to DynamoDB
    save_appointment(appointment_data)

    # Return success response
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'appointment created successfully',
            'appointment_id': appointment_data['appointment_id']
        })
    } 