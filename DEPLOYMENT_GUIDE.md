# 🔴 AI DevOps Copilot // Nothing OS Edition

This guide explains how to deploy your AI agent on EC2 with the **Nothing OS Aesthetic** and **Amazon Bedrock (Nova Pro)** integration.

## 1. Prerequisites
- **AWS Account** with Bedrock access.
- **Model Access**: Go to Amazon Bedrock Console -> Model Access -> Enable **Nova Pro**.
- **EC2 Instance**: Ubuntu 22.04+ (t3.medium recommended for better Streamlit performance).

## 2. Infrastructure Setup

### Create IAM Role
Create an IAM role for EC2 and attach this policy to allow it to speak to Bedrock:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "bedrock:InvokeModel",
            "Resource": "arn:aws:bedrock:*::foundation-model/amazon.nova-pro-v1:0"
        }
    ]
}
```

## 3. Deployment on EC2

### Step 1: System Update & Dependencies
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv git -y
```

### Step 2: Project Setup
```bash
# Clone or upload the project folder
mkdir ai-devops-agent && cd ai-devops-agent

# Set up environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install streamlit boto3 python-dotenv
```

### Step 3: Run the Application
To make the application stay running even after you close SSH, use `nohup`:
```bash
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 &
```

## 4. Testing & Verification
1. Open `http://<EC2-PUBLIC-IP>:8501`.
2. Observe the **Nothing OS** UI (Black background, Dot-matrix fonts, Red accents).
3. **Prompt Test**: "Create Terraform for an RDS cluster and a GitHub Actions pipeline to deploy to EKS."
4. Check the **COMPLIANCE_SCAN_PASS** section for automatic security auditing.

## 5. Why this works
- **Nova Pro Integration**: We use `inferenceConfig` with a low temperature (0.2) to ensure the code generated is syntactically perfect.
- **Dynamic CSS**: We injected Nothing OS fonts (Space Grotesk and Silkscreen) and color schemas directly into Streamlit for a premium look.
- **Resilient Logic**: The application includes error handling and a secondary mock fallback to ensure you never have a "broken demo."
