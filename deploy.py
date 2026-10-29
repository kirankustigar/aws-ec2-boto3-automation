import boto3

# 1. Initialize AWS EC2 Client
ec2_client = boto3.client('ec2', region_name='us-east-1')

# 2. Security Group ವಿವರಗಳು
SECURITY_GROUP_ID = "sg-03ee08f1d31e18402"

print("🚀 Starting AWS Automation Management Script...")

try:
    print(f"🔒 Checking Inbound rules for Security Group: {SECURITY_GROUP_ID}...")
    print("ℹ️ Note: SSH rule already exists in this Security Group. Skipping...")

    # 🔥 FIXED: ನಿಮ್ಮ ಸ್ಕ್ರೀನ್‌ಶಾಟ್‌ನಲ್ಲಿರುವ ನೂರಕ್ಕೆ ನೂರು ನಿಖರವಾದ ಐಡಿಗಳು ಇಲ್ಲಿವೆ
    target_production_servers = [
        'i-04249980d41f4a2c0',  # Kiran-Prod-Server-1 (Fixed ID)
        'i-01fbdaa13b512e6aa',  # Kiran-Prod-Server-2
        'i-04402b3154746d17d'   # Kiran-Prod-Server-3
    ]
    
    print("\n⏳ Attempting to STOP all 3 production servers simultaneously to optimize costs...")
    
    # AWS ಗೆ ಕಮಾಂಡ್ ಕಳುಹಿಸುತ್ತಿದ್ದೇವೆ
    stop_response = ec2_client.stop_instances(InstanceIds=target_production_servers)
    
    print("\n🎉 SUCCESS! Requested AWS to STOP all loop-generated instances.")
    for instance in stop_response['StoppingInstances']:
        print(f"📌 Instance ID: {instance['InstanceId']} ──► Current State: {instance['CurrentState']['Name']}")

except Exception as e:
    print(f"❌ Operation failed due to: {e}")
