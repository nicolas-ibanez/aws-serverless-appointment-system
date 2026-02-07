AWS Serverless Appointment System (Backend-Only)
Project Overview
This project is a high-performance, event-driven backend designed for automated appointment management. The focus is pure architecture, security, and scalability, intentionally avoiding frontend complexity to master the core principles of Cloud Engineering and prepare for the AWS SAA-C03 certification.

Core Engineering Objectives
Security First: Implementation of the Principle of Least Privilege (PoLP) across all resources.

Cost Efficiency: 100% Serverless architecture to stay within the AWS Free Tier and manage costs effectively.

Scalability: Design capable of handling thousands of requests using NoSQL and asynchronous processing.

Infrastructure as Code (IaC): Moving from manual configuration to automated deployments using Terraform or AWS CDK.

Tech Stack
Compute: AWS Lambda (Python 3.9+).

API Layer: Amazon API Gateway (REST API).

Database: Amazon DynamoDB (Single-table design for performance).

Security: IAM with PowerUserAccess (Dev environment) and custom restricted policies for services.

Monitoring: Amazon CloudWatch (Logs, Metrics, and Alarms).

Storage: Amazon S3 (Raw data backups and logs).

Project Roadmap 2026
Phase 1: Infrastructure & Security Foundations (CURRENT)
[x] Set up AWS Environment & IAM Security (PoLP implementation).

[ ] Configure AWS Budgets with real-time alerts ($120.00 USD credit management).

[ ] Deploy "Hello World" Lambda via AWS CLI to validate permissions.

Phase 2: Core API & Database Design
[ ] Design DynamoDB schema for appointments (Primary and Sort Keys definition).

[ ] Build CRUD operations (Create, Read, Update, Delete) using Python Boto3.

[ ] Implement API Gateway with Request Validation.

Phase 3: Automation & Reliability
[ ] Transition manual resources to Terraform scripts.

[ ] Implement structured logging and error handling in CloudWatch.

[ ] Optional/Future: External integrations (WhatsApp/Calendly) only after core architecture is bulletproof.

Author
Nicolás Ibañez Civil Engineering in Informatics Student at UNAB

Goal: Building technical excellence and high-value engineering criteria.
