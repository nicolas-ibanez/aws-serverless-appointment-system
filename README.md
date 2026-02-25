## ⚡️ AWS Serverless Appointment System

"Architecture over interface. Engineering over fashion."

## The Problem
Small clinics and service businesses in Latin America 
manage appointments via WhatsApp manually, losing 
30-40% of bookings due to no confirmation system. 
This backend solves that with a scalable, serverless API.

## Architecture
[diagrama simple aquí - lo construimos juntos]

API Gateway → Lambda (Python) → DynamoDB
                    ↓
                 S3 (audit logs)
                    ↓
              CloudWatch (alerts)

## Tech Decisions & Why
| Component     | Choice      | Rejected    | Reason                          |
|---------------|-------------|-------------|----------------------------------|
| Database      | DynamoDB    | RDS/MySQL   | No joins needed, pay-per-request|
| Compute       | Lambda      | EC2         | Traffic is sporadic, not 24/7   |
| IaC           | Terraform   | Console     | Reproducible, version-controlled|

## Security Model
- Each Lambda has its own IAM Role (not shared)
- Roles follow strict PoLP: only the permissions needed
- No hardcoded credentials, all via environment variables

## API Endpoints
POST /appointments     → Create appointment
GET  /appointments/{id} → Get by ID  
PUT  /appointments/{id} → Update status
DELETE /appointments/{id} → Cancel

## Current Status
- [x] IAM roles configured with PoLP
- [x] DynamoDB table with single-table design
- [ ] Lambda CRUD operations (in progress)
- [ ] API Gateway integration
- [ ] CloudWatch alarms
- [ ] Terraform migration

## Running Locally
aws lambda invoke --function-name createAppointment \
  --payload '{"patientId": "123", "date": "2026-03-01"}' \
  response.json
## 👨‍💻 Author
**Nicolás Ibañez**
*Civil Engineering in Informatics Student at UNAB*
> *Goal: Building technical excellence and high-value engineering criteria.*
