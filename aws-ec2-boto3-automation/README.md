# AWS Infrastructure Deployment Automation using Python Boto3

A professional DevOps automation script to dynamically update network security configurations and deploy EC2 instances within an existing custom AWS VPC infrastructure using Python's Boto3 SDK.

## 🚀 Features
- **Idempotent Security Rule Injection:** Automatically updates AWS Security Group Inbound rules to allow audited SSH (Port 22) access for incident resolution.
- **Targeted Subnet Deployment:** Launches scalable `t2.micro` Ubuntu Linux servers inside dedicated public enterprise subnets.
- **Automated Resource Tagging:** Dynamically attaches standardized metadata tags (`Name: Kiran-DevOps-Server`) for strict asset tracking.

## 🛠️ Infrastructure Context Used
- **VPC ID:** `vpc-07715cc72837aa11a`
- **Subnet ID:** `subnet-0091beed58ad9493d`
- **Security Group ID:** `sg-03ee08f1d31e18402`
- **Region:** `us-east-1`

## 📋 Prerequisites & Local Setup
1. **Install AWS CLI & Python Boto3:**
   ```bash
   pip install boto3
   ```
2. **Configure AWS Identity-Based Credentials:**
   Ensure your local environment has an IAM user configured with strict least-privilege IAM permissions.
   ```bash
   aws configure
   ```

## 💻 Usage
Simply execute the Python script to run the automated deployment pipeline:
```bash
python deploy.py
```
