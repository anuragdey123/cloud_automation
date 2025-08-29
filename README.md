# Cloud Automation with Python (Boto3)

This project provides Python scripts to automate common AWS operations using Boto3, including:
- Creating and terminating EC2 instances
- Creating and deleting S3 buckets
- Monitoring EC2 instance CPU metrics

## Prerequisites

### 1. Python Installation
- Python 3.8 or higher is required
- Verify installation:
  ```bash
  python --version
  ```

### 2. AWS Account Setup
- Create an AWS account if you don't have one
- Create an IAM user with programmatic access and the following permissions:
  - AmazonEC2FullAccess
  - AmazonS3FullAccess
  - CloudWatchReadOnlyAccess

### 3. AWS CLI Configuration
```bash
# Install AWS CLI (if not already installed)
# For Windows:
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

# Configure AWS credentials
aws configure
# Follow the prompts to enter:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region name (e.g., us-east-1)
# - Default output format (json)
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## Files

- `main.py` - Create EC2 instance and S3 bucket
- `monitoring.py` - Fetch CloudWatch CPU metrics for an EC2 instance
- `teardown.py` - Terminate EC2 instance and delete S3 bucket
- `config.json` - Configuration file (edit before running)
- `requirements.txt` - Python dependencies

## Setup

1. Clone this repository
   ```bash
   git clone https://github.com/yourusername/cloud_automation.git
   cd cloud_automation
   ```

2. Configure `config.json`:
   - Open `config.json` in a text editor
   - Update the following values:
     ```json
     {
         "region": "us-east-1",
         "instance_type": "t2.micro",
         "ami_id": "ami-0c55b159cbfafe1f0",  # Amazon Linux 2 AMI (us-east-1)
         "key_name": "your-key-pair-name",    # Must be created in AWS EC2 first
         "s3_bucket_name": "your-unique-bucket-name-12345",
         "instance_name": "automated-instance"
     }
     ```
   - **Important**: The S3 bucket name must be globally unique across all AWS accounts
   - To create a key pair:
     1. Go to AWS EC2 Console → Key Pairs → Create key pair
     2. Choose a name and download the .pem file
     3. Store it in a secure location with proper permissions:
        ```bash
        chmod 400 your-key-pair-name.pem
        ```
   - `region`: AWS region (e.g., us-east-1)
   - `instance_type`: EC2 instance type (e.g., t2.micro)
   - `ami_id`: AMI ID for the instance
   - `key_name`: Your EC2 key pair name
   - `s3_bucket_name`: Unique name for S3 bucket
   - `instance_name`: Name tag for the EC2 instance

## Usage Examples

### 1. Creating Resources
```bash
# Create EC2 instance and S3 bucket
python main.py

# Expected output:
# EC2 instance i-0123456789abcdef0 is launching...
# EC2 instance i-0123456789abcdef0 is now running
# Public IP: 54.123.45.67
# S3 bucket your-bucket-name created successfully
# Resource creation complete!
# EC2 Instance ID: i-0123456789abcdef0
# S3 Bucket Name: your-bucket-name
```

### 2. Monitoring Resources
```bash
# Monitor CPU usage of an EC2 instance
python monitoring.py
# When prompted, enter the instance ID (e.g., i-0123456789abcdef0)

# Sample output:
# CPU Utilization for instance i-0123456789abcdef0:
# Timestamp                    Avg %      Max %
# 2023-08-29 05:15:00          1.23       2.50
# 2023-08-29 05:16:00          1.10       1.50
# Press Ctrl+C to stop monitoring...
```

### 3. Cleaning Up Resources
```bash
# Terminate EC2 instance and delete S3 bucket
python teardown.py
# Follow the prompts to confirm resource deletion

# Expected output:
# Enter the EC2 Instance ID to terminate: i-0123456789abcdef0
# Termination initiated for instance i-0123456789abcdef0
# Instance i-0123456789abcdef0 has been terminated
# 
# Enter the S3 bucket name to delete [your-bucket-name]: 
# S3 bucket your-bucket-name has been deleted
# 
# Cleanup complete!
```

## Troubleshooting

### Common Issues and Solutions

#### 1. AWS Credentials Errors
```
botocore.exceptions.NoCredentialsError: Unable to locate credentials
```
- **Solution**: Ensure you've run `aws configure` and entered valid credentials
- Verify credentials in `~/.aws/credentials` (Linux/Mac) or `%UserProfile%\.aws\credentials` (Windows)

#### 2. Instance Launch Failures
```
An error occurred (InvalidKeyPair.NotFound) when calling the RunInstances operation: The key pair 'your-key-pair-name' does not exist
```
- **Solution**: 
  1. Create the key pair in AWS EC2 Console
  2. Download the .pem file
  3. Update `key_name` in `config.json`
  4. Set proper permissions: `chmod 400 your-key-pair-name.pem`

#### 3. S3 Bucket Name Already Exists
```
An error occurred (BucketAlreadyExists) when calling the CreateBucket operation: The requested bucket name is not available
```
- **Solution**: Choose a globally unique bucket name in `config.json`

#### 4. Region Mismatch
```
An error occurred (AuthFailure) when calling the RunInstances operation: AWS was not able to validate the provided access credentials
```
- **Solution**: Ensure the region in `config.json` matches the region where your resources exist

#### 5. Insufficient IAM Permissions
```
An error occurred (UnauthorizedOperation) when calling the RunInstances operation: You are not authorized to perform this operation.
```
- **Solution**: Attach the required IAM policies to your IAM user

## Notes

- The default AMI ID in `config.json` is for Amazon Linux 2 in us-east-1. Update it for your region.
- For different regions, find the appropriate AMI ID in the AWS Management Console.
- Monitor your AWS Free Tier usage to avoid unexpected charges.

## Security Best Practices

1. **Never commit sensitive information**:
   - Add `.aws/` to your `.gitignore`
   - Never commit `config.json` with actual credentials
   
2. **Use IAM roles for EC2 instances** in production instead of access keys

3. **Set up billing alerts** in AWS to monitor costs

4. **Regularly rotate your AWS access keys**

5. **Use VPC and Security Groups** to restrict access to your instances

## Support

For additional help, please open an issue in the GitHub repository or contact the maintainers.
