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
    # 4. Launch EC2 Instance inside the Public Subnet
    print(f"⏳ Launching EC2 Instance in Public Subnet ({PUBLIC_SUBNET_ID})...")
    
    instance_response = ec2_client.run_instances(
        ImageId=AMI_ID,
        InstanceType='t2.micro',
        MinCount=1,
        MaxCount=1,
        SubnetId=PUBLIC_SUBNET_ID,
        SecurityGroupIds=[SECURITY_GROUP_ID],
        KeyName=KEY_PAIR_NAME
    )
    
    # 🔥 FIXED LINE: Boto3 ಲಿಸ್ಟ್‌ನಿಂದ ಮೊದಲನೇ ಇನ್‌ಸ್ಟನ್ಸ್ ಐಡಿಯನ್ನು ಸರಿಯಾಗಿ ಹೊರತೆಗೆಯಲಾಗುತ್ತಿದೆ [0]
    instance_id = instance_response['Instances'][0]['InstanceId']
    
    print(f"\n🎉 SUCCESS! EC2 Instance Launched successfully.")
    print(f"📌 Instance ID: {instance_id}")
    print(f"🌐 VPC ID: {VPC_ID}")
    
    # 5. Add a Name Tag to the EC2 Instance
    ec2_client.create_tags(
        Resources=[instance_id],
        Tags=[{'Key': 'Name', 'Value': 'Kiran-DevOps-Server'}]
    )
    print("🏷️ Name Tag 'Kiran-DevOps-Server' attached to the instance.")

except Exception as e:
    print(f"❌ Deployment failed due to: {e}")
