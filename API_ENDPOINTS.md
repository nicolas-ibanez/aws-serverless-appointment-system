# API Endpoints

## Base URL
```
https://33sgjn5042.execute-api.us-east-1.amazonaws.com/dev
```

## Endpoints

### POST /appointments
Create a new appointment

**Request:**
```bash
Invoke-RestMethod -Uri "https://33sgjn5042.execute-api.us-east-1.amazonaws.com/dev/appointments" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"patient_name": "Carlos", "doctor_name": "Dr. Silva", "appointment_date": "2026-03-15", "appointment_time": "09:30"}'
```

**Response:**
```json
{
  "message": "appointment created successfully",
  "appointment_id": "APT-20260220123045"
}
```
### GET /appointments/{id}
Retrieve an appointment by ID

**Request:**
```bash
Invoke-RestMethod -Uri "https://33sgjn5042.execute-api.us-east-1.amazonaws.com/dev/appointments/APT-20260221224937" -Method Get
```

**Response:**
```json
{
  "appointment_id": "APT-20260221224937",
  "doctor_name": "Dr. Silva",
  "patient_name": "Carlos",
  "appointment_date": "2026-03-15",
  "appointment_time": "09:30",
  "state": "pending"
}
```
### PUT /appointments/{id}
Update the state of an appointment

**Request:**
```bash
Invoke-RestMethod -Uri "[https://33sgjn5042.execute-api.us-east-1.amazonaws.com/dev/appointments/APT-123456789](https://33sgjn5042.execute-api.us-east-1.amazonaws.com/dev/appointments/APT-123456789)" -Method Put -Headers @{"Content-Type"="application/json"} -Body '{"state": "confirmed"}'

**Response:**
{
  "message": "Appointment state updated successfully",
  "appointment_id": "APT-123456789",
  "new_state": "confirmed"
}

### PUT /appointments/{id}
Update the state of an appointment

**Request:**
```bash
Invoke-RestMethod -Uri "[https://33sgjn5042.execute-api.us-east-1.amazonaws.com/dev/appointments/APT-123456789](https://33sgjn5042.execute-api.us-east-1.amazonaws.com/dev/appointments/APT-123456789)" -Method Put -Headers @{"Content-Type"="application/json"} -Body '{"state": "confirmed"}'

**Response:**
{
  "message": "Appointment state updated successfully",
  "appointment_id": "APT-123456789",
  "new_state": "confirmed"
}

### DELETE /appointments/{id}
Delete an apointment

**Request:**
```bash
Invoke-RestMethod -Uri "[https://33sgjn5042.execute-api.us-east-1.amazonaws.com/dev/appointments/APT-123456789](https://33sgjn5042.execute-api.us-east-1.amazonaws.com/dev/appointments/APT-123456789)" -Method Delete

**Response:**
{
  "message": "Appointment deleted successfully",
  "appointment_id": "APT-123456789"
}
---

