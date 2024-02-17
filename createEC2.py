import boto3

ec2 = boto3.resource(
    'ec2',
    region_name='us-east-1'
)

# response = ec2.describe_instances()
# print(response)

ami_id = "ami-0c7217cdde317cfec"
key_name = "DevCSE546"
security_group_ids = ["sg-0ef331f308211b7ec"]

with open("cc-startup-script.txt","r") as file:
    user_data = file.read()

instance = ec2.create_instances(
    ImageId=ami_id,
    MinCount=1,
    MaxCount=1,
    InstanceType="t2.micro",
    KeyName=key_name,
    SecurityGroupIds=security_group_ids,
    UserData=user_data,
    TagSpecifications=[{'ResourceType':'instance',
                        'Tags': [{
                            'Key': 'Name',
                            'Value': 'web-instance' }]}]
)

instance[0].wait_until_running()

print("Instance ID:", instance[0].id)