import boto3
import json

def load_config():
    with open('config.json') as f:
        return json.load(f)

def terminate_ec2_instance(instance_id, region):
    """Terminate the specified EC2 instance"""
    ec2 = boto3.client('ec2', region_name=region)
    
    try:
        response = ec2.terminate_instances(InstanceIds=[instance_id])
        print(f"Termination initiated for instance {instance_id}")
        
        # Wait for the instance to be terminated
        waiter = ec2.get_waiter('instance_terminated')
        waiter.wait(InstanceIds=[instance_id])
        print(f"Instance {instance_id} has been terminated")
        
    except Exception as e:
        print(f"Error terminating instance {instance_id}: {str(e)}")
        raise

def delete_s3_bucket(bucket_name, region):
    """Delete the specified S3 bucket and all its contents"""
    s3 = boto3.client('s3', region_name=region)
    s3_resource = boto3.resource('s3', region_name=region)
    
    try:
        # Empty the bucket first
        bucket = s3_resource.Bucket(bucket_name)
        bucket.objects.all().delete()
        
        # Delete the bucket
        s3.delete_bucket(Bucket=bucket_name)
        print(f"S3 bucket {bucket_name} has been deleted")
        
    except s3.exceptions.NoSuchBucket:
        print(f"Bucket {bucket_name} does not exist")
    except Exception as e:
        print(f"Error deleting S3 bucket {bucket_name}: {str(e)}")
        raise

def main():
    print("Starting resource cleanup...")
    
    try:
        config = load_config()
        
        # Get instance ID from user
        instance_id = input("Enter the EC2 Instance ID to terminate (or press Enter to skip): ").strip()
        
        if instance_id:
            terminate_ec2_instance(instance_id, config['region'])
        
        # Get S3 bucket name from user
        bucket_name = input(f"\nEnter the S3 bucket name to delete [{config['s3_bucket_name']}]: ").strip() or config['s3_bucket_name']
        
        delete_s3_bucket(bucket_name, config['region'])
        
        print("\nCleanup complete!")
        
    except Exception as e:
        print(f"An error occurred during cleanup: {str(e)}")
        print("Please check the error message and try again.")

if __name__ == "__main__":
    main()
