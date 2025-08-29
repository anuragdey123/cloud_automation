import boto3
import datetime
import time

def get_cpu_utilization(instance_id, region='us-east-1', period=60, duration_minutes=60):
    """
    Fetch CPU utilization metrics for the specified EC2 instance
    """
    cloudwatch = boto3.client('cloudwatch', region_name=region)
    
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(minutes=duration_minutes)
    
    try:
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': instance_id
                },
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=period,
            Statistics=['Average', 'Maximum'],
            Unit='Percent'
        )
        
        datapoints = response.get('Datapoints', [])
        if not datapoints:
            print(f"No CPU metrics available for instance {instance_id}")
            return
            
        # Sort datapoints by timestamp (newest first)
        datapoints.sort(key=lambda x: x['Timestamp'], reverse=True)
        
        print(f"\nCPU Utilization for instance {instance_id}:")
        print("-" * 60)
        print(f"{'Timestamp':<30} {'Avg %':<10} {'Max %'}")
        print("-" * 60)
        
        for dp in datapoints:
            timestamp = dp['Timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            avg = dp.get('Average', 'N/A')
            max_val = dp.get('Maximum', 'N/A')
            print(f"{timestamp:<30} {avg:<10.2f} {max_val:.2f}")
            
    except Exception as e:
        print(f"Error fetching CPU metrics: {str(e)}")

def main():
    print("EC2 Instance CPU Monitoring")
    print("-" * 30)
    
    config = {}
    try:
        with open('config.json') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        config['region'] = 'us-east-1'
    
    instance_id = input("Enter EC2 Instance ID: ").strip()
    
    if not instance_id:
        print("Error: Instance ID cannot be empty")
        return
    
    try:
        while True:
            get_cpu_utilization(
                instance_id=instance_id,
                region=config.get('region', 'us-east-1'),
                period=60,
                duration_minutes=15
            )
            print("\nPress Ctrl+C to stop monitoring...")
            time.sleep(60)  # Update every minute
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import json  # Moved here to fix the NameError
    main()
