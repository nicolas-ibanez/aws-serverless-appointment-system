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

def get_appointment(appointment_id):
    """
    Retrives an appointment by ID from DunamoDB.

    args:
        appointment_id (str): unique appointment identifier

    returns:
        dict: appointment data or none if not found
    """
    response = table.get_item(Key={'appointment_id': appointment_id})
    return response.get('Item', None)

#Save the appointment
result = save_appointment(appointment_data)
print("Appointment saved successfully!")
print(f"Appointment ID: {appointment_data['appointment_id']}")

#Test reading the appointment we just created
print("\n--- Testing READ ---")
retrieved = get_appointment(appointment_data['appointment_id'])
if retrieved:
    print(f"Found appointment: patient: {retrieved['name_patient']} with Dr. {retrieved['name_doctor']}")
else:
    print("Appointment not found.")