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
    Updates the state of an existing appointment

    args:
        appointment_id (str): Unique appointment identifier
        new_state (str): New state value (confirmed/pending/cancelled)
    returns:
        dict: DynamoDB response
    """
    response = table.update_item(
        Key={'appointment_id': appointment_id},
        UpdateExpression="set #s = :new_state",
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

#Test updating the appointment
print("\n--- Testing UPDATE ---")
update_appointment_state(appointment_data['appointment_id'], "cancelled")
updated = get_appointment(appointment_data['appointment_id']) 
print(f"New state: {updated['state']}")

#Test deleting the appointment
print("\n--- Testing DELETE ---")
delete_appointment(appointment_data["appointment_id"])
returned = get_appointment(appointment_data['appointment_id'])
if not returned:        
    print("Appointment successfully deleted.")
else:   
    print("Failed to delete appointment.")
