import boto3 
from datetime import datetime


#connect to DynamoDB
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

appointment_data = {
    "appointment_id": generate_appointment_id(),
    "name_patient": "nicolas",
    "name_doctor": "batian",
    "date": "2026-02-16",
    "state": "confirmed"
}

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

#Save the appointment
result = save_appointment(appointment_data)
print("Appointment saved successfully!")
print(f"Appointment ID: {appointment_data['appointment_id']}")