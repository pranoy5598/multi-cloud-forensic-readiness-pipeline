# Multi-cloud-forensic-readiness-pipeline
Serverless multi-cloud forensic readiness framework using AWS CloudTrail, Azure Blob Storage, Microsoft Sentinel, and Defender.


---

## 📖 Overview

This project implements a fully serverless, multi-cloud security architecture designed to enhance forensic readiness through:

- Cross-cloud log redundancy
- SHA-256 integrity verification
- Real-time suspicious activity detection
- Microsoft Sentinel SIEM integration
- Automated incident creation via Microsoft Defender

![Architecture Diagram](architecture.png)

---

## 🏗️ Architecture

AWS CloudTrail → Amazon S3 → AWS Lambda (Upload + Hash)  
→ Azure Blob Storage → Azure Logic App → Azure Function  
→ Microsoft Sentinel → Microsoft Defender Incident

---

![Workflow Diagram](workflow.png)

## 🔐 Security Features

### Cross-Cloud Redundancy
CloudTrail logs are replicated from AWS to Azure.

### Integrity Assurance
Each log file is hashed using SHA-256.
A `.hash.txt` file is stored alongside the log.

### Real-Time Alerting
Suspicious API calls such as:
- DeleteTrail
- StopLogging
- Root login without MFA

Trigger:
- AWS SNS Email Alerts
- Microsoft Defender Incident Creation

---

## 📊 Results

- Detection latency < 3 seconds (AWS)
- Sentinel ingestion < 10 seconds
- 0 false positives in controlled testing
- Fully serverless architecture
- No third-party agents required

---

---

## ⚙️ Technologies Used

- AWS CloudTrail
- AWS Lambda
- Amazon S3
- AWS SNS
- Azure Blob Storage
- Azure Logic Apps
- Azure Functions
- Microsoft Sentinel
- Microsoft Defender
- Kusto Query Language (KQL)

---
## Project Overview

This project builds a fully serverless, multi-cloud security pipeline designed to improve forensic readiness and real-time threat detection across AWS and Microsoft Azure.

The foundation of the system is AWS CloudTrail, which records all account activity such as API calls, logins, and administrative changes. These logs are critical during investigations, but relying on a single cloud provider introduces risk. If an attacker gains privileged access, they could attempt to delete logs or disable logging entirely, weakening forensic visibility.

To solve this, I implemented cross-cloud log redundancy. CloudTrail logs are stored in an Amazon S3 bucket, where an event automatically triggers an AWS Lambda function whenever a new log file is created. This function calculates a SHA-256 hash of the log file to create a cryptographic fingerprint, then uploads both the original log and a corresponding .hash.txt file to Azure Blob Storage. This ensures that every AWS log has a secure copy in a separate cloud provider and that any tampering can be detected through hash verification.

In parallel, I implemented real-time detection logic inside AWS. A second Lambda function parses each CloudTrail log and checks for suspicious activity such as DeleteTrail, StopLogging, root logins without MFA, or access from flagged IP addresses. When triggered, the system immediately sends an alert through Amazon SNS. During testing, alerts were generated within seconds and produced no false positives in controlled scenarios.

To centralize monitoring, I integrated Microsoft Sentinel. Azure Logic Apps monitor the Blob container for new uploads and forward log records into Sentinel using the Log Analytics Data Collector API. Custom KQL rules analyze the ingested logs and automatically create security incidents in Microsoft Defender when high-risk behavior is detected. Log ingestion typically occurred in under ten seconds.

**The entire architecture is serverless and event-driven. It uses only native cloud services—no virtual machines, no persistent compute, and no third-party agents. The design follows Zero Trust principles by assuming breach, verifying log integrity, separating redundancy from detection, and maintaining cross-provider resilience.
---

## 📈 Future Improvements

- ML-based anomaly detection
- Periodic hash revalidation
- Blockchain anchoring for high-value logs
- SOAR integration


