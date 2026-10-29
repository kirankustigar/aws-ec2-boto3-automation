
import boto3
# 1. Initialize AWS EC2 Client (us-east-1 ರೀಜನ್ ಸೆಟ್ ಮಾಡಲಾಗಿದೆ)
ec2_client = boto3.client('ec2', region_name='us-east-1')
# 2. ನಿಮ್ಮ AWS ಎನ್ವಿರಾನ್ಮೆಂಟ್‌ನ ನಿಖರವಾದ ಐಡಿಗಳು (Hardcoded Details)
VPC_ID = "vpc-07715cc72837aa11a"
PUBLIC_SUBNET_ID = "subnet-0091beed58ad9493d"
SECURITY_GROUP_ID = "sg-03ee08f1d31e18402"
KEY_PAIR_NAME = "my-devops-key"
AMI_ID = "ami-0866a3c8686eaeeba"  # Ubuntu 24.04 LTS Image
print("🚀 Starting AWS Automation Deployment Using Existing Infrastructure...")
try:
    # 3. Security Group Rules Update (SSH Access)
    print(f"🔒 Checking Inbound rules for Security Group: {SECURITY_GROUP_ID}...")
    
    ec2_client.authorize_security_group_ingress(
        GroupId=SECURITY_GROUP_ID,
        IpPermissions=[
            {
                'IpProtocol': 'tcp',
                'FromPort': 22,
                'ToPort': 22,
                'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'Allow SSH for DevOps Automation'}]
            }
        ]
    )
    print("✅ Inbound rule added successfully.")
except ec2_client.exceptions.ClientError as e:
    if 'InvalidPermission.Duplicate' in str(e):
        print("ℹ️ Note: SSH rule already exists in this Security Group. Skipping...")
    else:
        print(f"❌ Error updating Security Group: {e}")
try:
    # 4. Stop the Existing EC2 Instances (ನಿಮ್ಮ ಲೈವ್ ಇನ್‌ಸ್ಟನ್ಸ್‌ಗಳನ್ನು ನಿಲ್ಲಿಸುತ್ತಿದ್ದೇವೆ)
    print("⏳ Attempting to STOP the running EC2 Instances to optimize costs...")
    
    # ನಾವು ಲಾಂಚ್ ಮಾಡಿದ್ದ ಆ ಎರಡು ಇನ್‌ಸ್ಟನ್ಸ್ ಐಡಿಗಳನ್ನು ಇಲ್ಲಿ ನೀಡಿದ್ದೇವೆ
    target_instances = ['i-040d3ab8fa9f814b6', 'i-0fe8a24dfff94a622']
    
    # AWS ಗೆ ಇನ್‌ಸ್ಟನ್ಸ್‌ಗಳನ್ನು ನಿಲ್ಲಿಸಲು ಕಮಾಂಡ್ ಕಳುಹಿಸುತ್ತಿದ್ದೇವೆ
    stop_response = ec2_client.stop_instances(InstanceIds=target_instances)
    
    print("\n🎉 SUCCESS! EC2 Instances have been requested to STOP.")
    for instance in stop_response['StoppingInstances']:
        print(f"📌 Instance ID: {instance['InstanceId']} ──► Current State: {instance['CurrentState']['Name']}")

except Exception as e:
    print(f"❌ Stop Operation failed due to: {e}")
