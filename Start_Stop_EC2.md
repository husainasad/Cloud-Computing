We can make a small addition to our project which is to start/stop resources such as EC2 at a specified time. For this we would be using AWS Labda and Eventbridge. The steps mentioned below are to be followed with an assumption that the EC2 instance has already been created and loosely based on [this](https://medium.com/@srijaanaparthy/automating-ec2-instance-start-and-stop-schedule-using-aws-lambda-and-amazon-eventbridge-988b0843d010) medium article.

## Step 1: Create IAM Policy
Create an IAM policy with the following JSON:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:Start*",
                "ec2:Stop*"
            ],
            "Resource": "arn:aws:ec2:*:*:*"
        }
    ]
}
```
This policy would allow the user/role to perform specific actions on CloudWatch Logs and EC2 resources

## Step 2: Create IAM Role
Create an IAM role and attach the IAM policy created above to the role. Also make sure the trusted relationships of the role should look like:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "lambda.amazonaws.com",
                    "scheduler.amazonaws.com"
                ]
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

The above code provides the Lambda and Scheduler services access to assume the role.

## Step 3: Create Lambda Functions
Create Lambda function and add the IAM role created above to the function. </br>

Lambda function to start EC2 service:
```
import boto3
region = 'us-east-1'
instances = ['i-12524cb6de4f78g9h', 'i-09ce8b2d7eccf6d26']
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    ec2.start_instances(InstanceIds=instances)
    print('started your instances: ' + str(instances))
```

Lambda function to stop EC2 service:
```
import boto3
region = 'ap-south-1'
instances = ['i-12524cb6de4f78g9h', 'i-09ce8b2d7eccf6d26']
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    ec2.stop_instances(InstanceIds=instances)
    print('stopped your instances: ' + str(instances))
```

Once the lambda function is created, deploy the function and test it.

## Create EventBridge Rule
Create EventBridge rule and use cron expression to define the funtion trigger schedule. </br>
Choose the lambda function target to be scheduled. <br>
All done