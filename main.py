import boto3
import json
import time

def load_config():
    with open('config.json') as f:
        return json.load(f)

def create_ec2_instance():
    config = load_config()
    ec2 = boto3.client('ec2', region_name=config['region'])
    
    try:
        response = ec2.run_instances(
            ImageId=config['ami_id'],
            InstanceType=config['instance_type'],
            KeyName=config['key_name'],
            MinCount=1,
            MaxCount=1,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': config['instance_name']},
                    ]
                },
            ]
        )
        
        instance_id = response['Instances'][0]['InstanceId']
        print(f"EC2 instance {instance_id} is launching...")
        
        # Wait for the instance to be running
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        
        # Get the public IP address
        instance = ec2.describe_instances(InstanceIds=[instance_id])
        public_ip = instance['Reservations'][0]['Instances'][0].get('PublicIpAddress')
        
        print(f"EC2 instance {instance_id} is now running")
        if public_ip:
            print(f"Public IP: {public_ip}")
            
        return instance_id
        
    except Exception as e:
        print(f"Error creating EC2 instance: {str(e)}")
        raise

def create_s3_bucket():
    config = load_config()
    s3 = boto3.client('s3', region_name=config['region'])
    
    try:
        # For regions other than us-east-1, you need to specify LocationConstraint
        if config['region'] == 'us-east-1':
            s3.create_bucket(Bucket=config['s3_bucket_name'])
        else:
            location = {'LocationConstraint': config['region']}
            s3.create_bucket(
                Bucket=config['s3_bucket_name'],
                CreateBucketConfiguration=location
            )
            
        print(f"S3 bucket {config['s3_bucket_name']} created successfully")
        return config['s3_bucket_name']
        
    except s3.exceptions.BucketAlreadyExists:
        print(f"Bucket {config['s3_bucket_name']} already exists")
        return None
    except Exception as e:
        print(f"Error creating S3 bucket: {str(e)}")
        raise

def main():
    print("Starting cloud resource creation...")
    
    try:
        # Create EC2 instance
        instance_id = create_ec2_instance()
        
        # Create S3 bucket
        bucket_name = create_s3_bucket()
        
        print("\nResource creation complete!")
        print(f"EC2 Instance ID: {instance_id}")
        if bucket_name:
            print(f"S3 Bucket Name: {bucket_name}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Cleaning up any created resources...")
        # Add cleanup logic if needed

if __name__ == "__main__":
    main()
