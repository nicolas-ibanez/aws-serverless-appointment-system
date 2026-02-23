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

---

## Coming Soon
- GET /appointments/{id}
- PUT /appointments/{id}
- DELETE /appointments/{id}