# AWS Serverless Appointment System - Project Roadmap

## I. Strategic Purpose

### Real Objective
Demonstrate serverless architecture design, cost optimization, and production-grade system development using industry-standard AWS services. This project proves technical decision-making ability and infrastructure management skills required for cloud engineering roles.

### Corporate Problem
Small clinics in Latin America manage appointments manually via WhatsApp, losing 30-40% of bookings due to lack of confirmation systems, double-bookings, and no automated reminders. This serverless backend solves that with a scalable, low-cost API.

### Positioning Goal
Build a portfolio piece defendable in technical English for:
- Internship applications in Chile (August 2026)
- AWS Solutions Architect Associate certification (April 2026)
- Future remote work opportunities with international companies

---

## II. Technical Architecture

### Stack Overview
**Zero frontend** - Pure backend and infrastructure demonstrating cloud-native patterns.

### Components

**Entry Point: API Gateway (REST API)**
- Receives HTTP requests from any client
- Handles request validation and routing
- Integrates directly with Lambda functions
- No server management required

**Core Processing: AWS Lambda (Python 3.9+)**
- Function: `lambda_handler(event, context)` format
- Operations: CREATE, READ, UPDATE, DELETE appointments
- Stateless execution (no local state between invocations)
- Auto-scaling from 0 to thousands of concurrent executions

**Data Layer: Amazon DynamoDB**
- Table: `AppointmentsTable`
- Partition Key: `appointment_id` (timestamp-based UUID)
- Schema: patient_name, doctor_name, appointment_date, appointment_time, state
- Pay-per-request billing (no provisioned capacity)
- Single-digit millisecond latency

**Why DynamoDB over RDS?**
1. No relational joins needed (simple key-value access)
2. Pay-per-request vs always-running database server
3. Automatic scaling without configuration
4. Better fit for sporadic traffic patterns

**Security: IAM Roles**
- Principle of Least Privilege applied
- Each Lambda has minimum required permissions
- No hardcoded AWS credentials in code
- Role: Lambda execution role with DynamoDB PutItem/GetItem/UpdateItem/DeleteItem only

**Observability: CloudWatch**
- Automatic log collection from Lambda
- Custom metrics for API performance
- Alarms for error rates and latency spikes
- Structured JSON logging for debugging

**Infrastructure as Code: Terraform**
- All resources defined in `.tf` files
- Reproducible deployments across environments
- Version-controlled infrastructure changes
- Enables disaster recovery and multi-region deployment

---

## III. Current State

### Completed ✅
- [x] DynamoDB table designed with proper Partition Key strategy
- [x] Python CRUD operations (save, get, update, delete) tested locally
- [x] Lambda handler adapted for AWS environment
- [x] CREATE function deployed to AWS Lambda
- [x] Boto3 integration functional
- [x] Git repository with .gitignore protecting credentials
- [x] Basic project documentation (PROJECT.md)
- [x] API Gateway REST API created ← New
- [x] POST /appointments endpoint functional ← New
- [x] Deployed to dev stage ← New
- [x] Tested from internet with PowerShell ← New

### In Progress 🚧
- [ ] API Gateway REST API creation
- [ ] API Gateway + Lambda integration
- [ ] GET, UPDATE, DELETE endpoints deployment
- [ ] CloudWatch logging configuration
- [ ] Error handling and input validation

### Pending ⏳
- [ ] Terraform infrastructure migration (from manual to IaC)
- [ ] Comprehensive README in English with setup instructions
- [ ] Architecture diagram (draw.io or Excalidraw)
- [ ] Postman collection for API testing
- [ ] Dead Letter Queue for failed invocations

---

## IV. Engineering Criteria

### Scalability
System handles 1 to 100,000+ requests without manual intervention. Lambda auto-scales horizontally, DynamoDB adapts to traffic patterns. No bottlenecks from fixed server capacity.

### Cost Optimization
- AWS Free Tier only (Lambda: 1M requests/month, DynamoDB: 25GB storage)
- Pay-per-execution model (no idle costs)
- No EC2 instances running 24/7
- Estimated cost: $0/month for development traffic

### Resilience
- Structured CloudWatch logs for rapid debugging
- Error handling with try-catch blocks
- Input validation before DynamoDB writes
- Future: Dead Letter Queues for failed Lambda invocations

### Professional Quality
- Code follows Python PEP 8 style guide
- Functions have docstrings explaining purpose and parameters
- Git commits use Conventional Commits format (feat:, fix:, docs:)
- Every architectural decision documented and justified

---

## V. Execution Timeline

### February 2026 (Current)
**Week 3 (Feb 17-23):**
- ✅ DynamoDB table created
- ✅ Lambda CRUD functions written
- ✅ CREATE endpoint deployed
- 🚧 API Gateway integration
- 🚧 Test via Postman/curl

**Week 4 (Feb 24-28):**
- Complete GET, UPDATE, DELETE endpoints
- CloudWatch logging setup
- Error handling implementation

### March 2026
**Week 1-2:**
- Begin Terraform conversion (manual resources → IaC)
- Write comprehensive README in English
- Create architecture diagram

**Week 3-4:**
- Finalize Terraform scripts
- Add Postman collection
- Project presentation-ready

### April 2026
- **April 15:** AWS SAA-C03 Certification Exam
- Project fully defended in technical English
- GitHub portfolio polished

---

## VI. Learning Alignment with AWS SAA-C03

This project directly covers these certification exam domains:

**Domain 1: Design Secure Architectures (30%)**
- IAM roles and policies (Principle of Least Privilege)
- Data encryption at rest (DynamoDB encryption)

**Domain 2: Design Resilient Architectures (26%)**
- Serverless patterns (Lambda + API Gateway + DynamoDB)
- Decoupling components (stateless Lambda functions)

**Domain 3: Design High-Performing Architectures (24%)**
- Caching strategies (future: API Gateway caching)
- Database selection (DynamoDB for key-value access)

**Domain 4: Design Cost-Optimized Architectures (20%)**
- Serverless vs EC2 cost comparison
- Pay-per-request pricing models
- Free Tier optimization

---

## VII. Technical Decisions Log

### Why DynamoDB over RDS (PostgreSQL/MySQL)?
**Decision:** DynamoDB NoSQL

**Reasoning:**
1. **Access Pattern:** Simple key-value lookups by appointment_id. No complex joins or aggregations needed.
2. **Cost:** Pay-per-request ($0.25 per million reads in Free Tier) vs RDS minimum $15/month for smallest instance running 24/7.
3. **Scalability:** Auto-scales without provisioning. RDS requires manual instance resizing.
4. **Operations:** No database administration, backups, or patching required.

**Trade-off Accepted:** Cannot perform complex SQL queries. Acceptable because use case doesn't require them.

---

### Why Lambda over EC2?
**Decision:** AWS Lambda

**Reasoning:**
1. **Traffic Pattern:** Clinic appointments are sporadic (peak hours, quiet nights). Lambda scales to zero during idle periods.
2. **Cost:** $0.20 per 1M requests vs EC2 t2.micro $8.50/month running 24/7.
3. **Maintenance:** No OS patching, security updates, or server management.
4. **Deployment:** Code-only deploys via zip file. No server provisioning.

**Trade-off Accepted:** 15-minute execution limit. Acceptable because appointment operations complete in <500ms.

---

### Why API Gateway REST API vs HTTP API?
**Decision:** REST API (initially, may migrate to HTTP API later)

**Reasoning:**
1. **Learning:** REST API has more features for educational purposes (request validation, API keys, usage plans).
2. **Certification:** AWS SAA-C03 focuses more on REST API patterns.
3. **Future:** Can migrate to HTTP API (70% cheaper) once fundamentals are mastered.

**Trade-off Accepted:** Slightly higher cost ($3.50 vs $1 per million requests). Acceptable for learning project.

---

## VIII. Success Metrics

### Technical Metrics
- [ ] All CRUD operations functional via HTTP API
- [ ] Average response time < 300ms (p95 < 500ms)
- [ ] Zero AWS charges beyond Free Tier limits
- [ ] 100% infrastructure reproducible via Terraform
- [ ] Zero hardcoded credentials in repository

### Professional Metrics
- [ ] Can explain every architectural decision in English without notes
- [ ] Can deploy entire system from scratch in < 20 minutes using Terraform
- [ ] Can debug production issues using only CloudWatch logs
- [ ] GitHub repository meets industry standards (README, .gitignore, conventional commits)

---

## IX. Immediate Next Steps

**This Week (Feb 17-23, 2026):**
1. ✅ Complete API Gateway REST API creation
2. ✅ Connect API Gateway to Lambda (CREATE function)
3. ✅ Test with Postman: `POST /appointments`
4. Document API endpoint in README

**Next Week (Feb 24-28, 2026):**
1. Deploy GET, UPDATE, DELETE Lambda functions
2. Create API Gateway routes for each operation
3. Add CloudWatch Logs integration
4. Begin AWS SAA-C03 study (30 min/day - Stephane Maarek course)

**Study Schedule Parallel to Project:**
- **Mon-Thu:** 30 min AWS course + 2 hours project work
- **Fri-Sun:** 1 hour AWS course + 4 hours project deep work
- **Daily:** 1 hour English (series + technical reading)

---

## X. Post-Project Evolution

Once this project is complete and defended (April 2026), the next project will be:

**Project 2: Event-Driven Notification System**
- Amazon SQS (message queues)
- Amazon SNS (pub/sub notifications)
- AWS EventBridge (event routing)
- Step Functions (workflow orchestration)

**Purpose:** Learn asynchronous architectures and event-driven patterns (mid-level engineer skill).

This establishes expertise in **Cloud Backend Engineering** specialization.