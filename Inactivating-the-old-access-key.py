import json
import boto3
import os

iam = boto3.client('iam')
secretsmanager = boto3.client('secretsmanager')

def lambda_handler(event, context):
    
    vsecret = os.getenv('secrets')
    secret_list = vsecret.split(';')

    for secret in secret_list:
        get_secret = secretsmanager.get_secret_value(SecretId=secret)
        secret_details = json.loads(get_secret['SecretString'])

        print("For user - " + secret_details['UserName'] + ", Access & Secret keys will be inactivated.")
        
        # Extracting the key details from IAM
        key_response = iam.list_access_keys(UserName=secret_details['UserName'])
        
        # Existing Key Inactivation
        for key in key_response['AccessKeyMetadata']:
            if key['Status'] == 'Active':
                iam.update_access_key(AccessKeyId=key['AccessKeyId'], Status='Inactive',UserName=key['UserName'])
                print(key['AccessKeyId'] + " key of " + key['UserName'] + " has been inactivated.")    
                   

    return "Process key creation & secret update has completed successfully."
