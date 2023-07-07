import boto3
import time

aws_access_key_id = ''
aws_secret_access_key = ''
region = 'us-east-2'
application_name = 'helloworld'
environment_name = 'venv'
version_label = 'v1'
app_zip_file = 'helloworld.zip'
bucket_name = 'elasticbeanstalk-us-east-2-399539668072'
file_path = 'helloworld.zip'
s3_key = 'helloworld.zip'


def create_application():
    elasticbeanstalk_client = boto3.client('elasticbeanstalk', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    response = elasticbeanstalk_client.create_application(ApplicationName=application_name)
    print('Application created successfully.')


def create_environment():
    elasticbeanstalk_client = boto3.client('elasticbeanstalk', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    response = elasticbeanstalk_client.list_available_solution_stacks()
    solution_stacks = response['SolutionStacks']
    solution_stack_name = '64bit Amazon Linux 2023 v4.0.2 running Python 3.11'
    response = elasticbeanstalk_client.create_environment(
        ApplicationName=application_name,
        EnvironmentName=environment_name,
        SolutionStackName=solution_stack_name,
        VersionLabel=version_label,
        OptionSettings=[
            {
                'Namespace': 'aws:autoscaling:launchconfiguration',
                'OptionName': 'IamInstanceProfile',
                'Value': 'arn:aws:iam::399539668072:role/service-role/aws-elasticbeanstalk-service-role'
            }
        ]
    )
    print('Environment created successfully.')


def upload_file_to_s3(bucket_name, file_path, s3_key):
    s3_client = boto3.client('s3', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    s3_client.upload_file(file_path, bucket_name, s3_key)
    print('File uploaded successfully.')


def upload_application_version():
    elasticbeanstalk_client = boto3.client('elasticbeanstalk', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    try:
        elasticbeanstalk_client.delete_application_version(
            ApplicationName=application_name,
            VersionLabel=version_label
        )
        print('Previous application version deleted.')
    except elasticbeanstalk_client.exceptions.SourceBundleDeletionFailureException:
        print('Previous application version not found.')
    response = elasticbeanstalk_client.create_application_version(
        ApplicationName=application_name,
        VersionLabel=version_label,
        SourceBundle={
            'S3Bucket': 'elasticbeanstalk-us-east-2-399539668072',
            'S3Key': 'helloworld.zip'
        }
    )
    print('Application version uploaded successfully.')


def update_environment():
    elasticbeanstalk_client = boto3.client('elasticbeanstalk', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    response = elasticbeanstalk_client.update_environment(
        ApplicationName=application_name,
        EnvironmentName=environment_name,
        VersionLabel=version_label
    )
    print('Environment update initiated.')


def wait_for_environment_ready():
    elasticbeanstalk_client = boto3.client('elasticbeanstalk', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    while True:
        response = elasticbeanstalk_client.describe_environments(
            ApplicationName=application_name,
            EnvironmentNames=[environment_name]
        )
        status = response['Environments'][0]['Status']
        if status == 'Ready':
            break
        time.sleep(10)
    print('Deployment complete.')



create_application()
upload_file_to_s3(bucket_name, file_path, s3_key)
upload_application_version()
create_environment()
wait_for_environment_ready()
update_environment()

