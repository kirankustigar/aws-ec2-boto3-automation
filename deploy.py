import boto3

# 1. Initialize AWS EC2 Client
ec2_client = boto3.client('ec2', region_name='us-east-1')

# 2. ನಿಮ್ಮ ಕನ್ಫರ್ಮ್ಡ್ ಇನ್ಫ್ರಾಸ್ಟ್ರಕ್ಚರ್ ವಿವರಗಳು
VPC_ID = "vpc-07715cc72837aa11a"
PUBLIC_SUBNET_ID = "subnet-0091beed58ad9493d"
SECURITY_GROUP_ID = "sg-03ee08f1d31e18402"
KEY_PAIR_NAME = "my-devops-key"
AMI_ID = "ami-0866a3c8686eaeeba"  # Ubuntu 24.04 LTS

# 🔥 CONFIGURATION: ನಿಮಗೆ ಎಷ್ಟು ಸರ್ವರ್ ಬೇಕೋ ಆ ಸಂಖ್ಯೆಯನ್ನು ಇಲ್ಲಿ ಸೆಟ್ ಮಾಡಿ!
NUMBER_OF_SERVERS = 3 

print(f"🚀 Starting Bulk Infrastructure Provisioning for {NUMBER_OF_SERVERS} Servers...")

# 3. Python For Loop ಬಳಸಿ ಒಂದೊಂದಾಗಿ ಸರ್ವರ್ ಲಾಂಚ್ ಮಾಡುವುದು
for i in range(1, NUMBER_OF_SERVERS + 1):
    try:
        # ಪ್ರತಿಯೊಂದು ಸರ್ವರ್‌ಗೂ ವಿಶಿಷ್ಟವಾದ ಹೆಸರನ್ನು ಕ್ರಿಯೇಟ್ ಮಾಡುತ್ತಿದ್ದೇವೆ (e.g., Kiran-Prod-Server-1)
        custom_server_name = f"Kiran-Prod-Server-{i}"
        print(f"\n⏳ Provisioning {custom_server_name} inside Public Subnet...")
        
        # EC2 ಲಾಂಚ್ ಕಮಾಂಡ್
        instance_response = ec2_client.run_instances(
            ImageId=AMI_ID,
            InstanceType='t2.micro',
            MinCount=1,
            MaxCount=1,
            SubnetId=PUBLIC_SUBNET_ID,
            SecurityGroupIds=[SECURITY_GROUP_ID],
            KeyName=KEY_PAIR_NAME
        )
        
        # ಇನ್‌ಸ್ಟನ್ಸ್ ಐಡಿ ಹೊರತೆಗೆಯುವುದು
        instance_id = instance_response['Instances'][0]['InstanceId']
        print(f"✅ Launched Successfully! Instance ID: {instance_id}")
        
        # ಲೂಪ್ ಒಳಗಡೆಯೇ ಆಯಾ ಸರ್ವರ್‌ಗೆ ಮ್ಯಾಪ್ ಆಗುವ ಕಸ್ಟಮ್ ನೇಮ್ ಟ್ಯಾಗ್ ಅಟ್ಯಾಚ್ ಮಾಡುವುದು
        ec2_client.create_tags(
            Resources=[instance_id],
            Tags=[{'Key': 'Name', 'Value': custom_server_name}]
        )
        print(f"🏷️ Tagged as: '{custom_server_name}'")
        
    except Exception as e:
        print(f"❌ Failed to launch Server-{i} due to: {e}")

print("\n🎉 BULK DEPLOYMENT COMPLETE! All servers are scaling up in AWS Console.")
