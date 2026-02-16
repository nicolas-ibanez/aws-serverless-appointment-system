appointment_data = {
    "name_patient": "nicolas",
    "name_doctor": "bastian",
    "date": "2026-02-16",
    "state": "confirmed"
                   }


def appointment(name_patient, name_doctor, date, state):
    return f"Appointment for {name_patient} with Dr. {name_doctor} on {date} is {state}."
print(appointment(**appointment_data))