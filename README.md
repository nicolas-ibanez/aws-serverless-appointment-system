# ⚡️ AWS Serverless Appointment System (Backend-Only)

> **"Architecture over interface. Engineering over fashion."**

---

## 🎯 Project Overview
This project is a high-performance, event-driven backend designed for automated appointment management. 

The focus is **pure architecture, security, and scalability**, intentionally avoiding frontend complexity to master the core principles of Cloud Engineering and prepare for the **AWS SAA-C03 certification**.

---

## 🛠 Tech Stack & Infrastructure

| Component | Service | Role |
| :--- | :--- | :--- |
| **Compute** | `AWS Lambda` | Serverless Python 3.9+ logic |
| **API Layer** | `API Gateway` | RESTful entry point & validation |
| **Database** | `DynamoDB` | Single-table design for high performance |
| **Security** | `IAM` | PowerUserAccess + Custom PoLP policies |
| **Storage** | `Amazon S3` | Raw data backups & audit logs |
| **Monitoring** | `CloudWatch` | Real-time logs, metrics, and alarms |

---

## 🏗 Core Engineering Objectives

* **🛡 Security First**: Strict implementation of the **Principle of Least Privilege (PoLP)** across all resources.
* **💸 Cost Efficiency**: 100% Serverless architecture to remain within the **AWS Free Tier**.
* **🚀 Scalability**: Async processing designed to handle thousands of concurrent requests.
* **🤖 Infrastructure as Code (IaC)**: Evolution from manual config to **Terraform/CDK** deployments.

---

## 🗺 Project Roadmap 2026

### **Phase 1: Foundations (CURRENT)**
- [x] Set up AWS Environment & IAM Security (PoLP).
- [ ] Configure **AWS Budgets** with real-time alerts ($120 USD credit management).
- [ ] Deploy "Hello World" Lambda via **AWS CLI** to validate permissions.

### **Phase 2: Core API & Data**
- [ ] Design **DynamoDB schema** (Primary & Sort Keys definition).
- [ ] Build CRUD operations using Python **Boto3**.
- [ ] Implement API Gateway Request Validation.

### **Phase 3: Automation**
- [ ] Transition manual resources to **Terraform** scripts.
- [ ] Implement structured logging & error handling in CloudWatch.
- [ ] *Future:* External API integrations (WhatsApp/Calendly).

---

## 👨‍💻 Author
**Nicolás Ibañez**
*Civil Engineering in Informatics Student at UNAB*
> *Goal: Building technical excellence and high-value engineering criteria.*
