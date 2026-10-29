import boto3

# 1. Initialize AWS EC2 Client (ನಿಮ್ಮ ರೀಜನ್ us-east-1 ಆಗಿರುವುದರಿಂದ ಇಲ್ಲಿ ಕಡ್ಡಾಯವಾಗಿ ನೀಡಲಾಗಿದೆ)
ec2_client = boto3.client('ec2', region_name='us-east-1')

# 2. ಪ್ರಸ್ತುತ ಚಾಲ್ತಿಯಲ್ಲಿರುವ ನಿಮ್ಮ ರಿಸೋರ್ಸ್ ಐಡಿಗಳು
VPC_ID = "vpc-07715cc72837aa11a"
PUBLIC_SUBNET_ID = "subnet-0091beed58ad9493d"
SECURITY_GROUP_ID = "sg-03ee08f1d31e18402"

print("🚀 Starting AWS Automation Deployment Using Existing Infrastructure...")

try:
    # 3. Security Group Rules Update (SSH Access)
    # ಇನ್ಸಿಡೆಂಟ್ ಮ್ಯಾನೇಜ್ಮೆಂಟ್ ಮತ್ತು ಟ್ರಬಲ್‌ಶೂಟಿಂಗ್ ಮಾಡಲು ಪೋರ್ಟ್ 22 (SSH) ಅನ್ನು ಈ ಸೆಕ್ಯೂರಿಟಿ ಗ್ರೂಪ್‌ಗೆ ಓಪನ್ ಮಾಡುತ್ತಿದ್ದೇವೆ.
    print(f"🔒 Checking and updating Inbound rules for Security Group: {SECURITY_GROUP_ID}...")
    
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
    print("✅ Inbound rule added successfully (or already exists).")
except ec2_client.exceptions.ClientError as e:
    if 'InvalidPermission.Duplicate' in str(e):
        print("ℹ️ Note: SSH rule already exists in this Security Group. Skipping...")
    else:
        print(f"❌ Error updating Security Group: {e}")

try:
    # 4. Launch EC2 Instance inside the Public Subnet
    # ಗಮನಿಸಿ: ami-0866a3c8686eaeeba ಎನ್ನುವುದು us-east-1 ರೀಜನ್‌ನ ಅಧಿಕೃತ Ubuntu 24.04 LTS AMI ಐಡಿಯಾಗಿದೆ.
    print(f"⏳ Launching EC2 Instance in Public Subnet ({PUBLIC_SUBNET_ID})...")
    
    instance_response = ec2_client.run_instances(
        ImageId='ami-0866a3c8686eaeeba',  # Ubuntu 24.04 AMI ID for us-east-1
        InstanceType='t2.micro',          # Free tier eligible instance type
        MinCount=1,
        MaxCount=1,
        SubnetId=PUBLIC_SUBNET_ID,
        SecurityGroupIds=[SECURITY_GROUP_ID],
        KeyName='my-devops-key'           # ⚠️ ನಿಮ್ಮ AWS ಕನ್ಸೋಲ್‌ನಲ್ಲಿರುವ Key Pair ಹೆಸರನ್ನು ಇಲ್ಲಿ ಬದಲಾಯಿಸಿ!
    )
    
    instance_id = instance_response['Instances']['InstanceId']
    print(f"\n🎉 SUCCESS! EC2 Instance Launched successfully.")
    print(f"📌 Instance ID: {instance_id}")
    print(f"🌐 VPC ID: {VPC_ID}")
    
    # 5. Add a Name Tag to the newly created EC2 Instance
    # ಸರ್ವರ್ ಅನ್ನು ಸುಲಭವಾಗಿ ಗುರುತಿಸಲು 'Kiran-DevOps-Server' ಎಂದು ಹೆಸರಿಸುತ್ತಿದ್ದೇವೆ.
    ec2_client.create_tags(
        Resources=[instance_id],
        Tags=[{'Key': 'Name', 'Value': 'Kiran-DevOps-Server'}]
    )
    print("🏷️ Name Tag 'Kiran-DevOps-Server' attached to the instance.")

except Exception as e:
    print(f"❌ Deployment failed due to: {e}")
