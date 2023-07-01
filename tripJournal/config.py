import boto3


def initialize_boto3():
    # Inizializza STS utilizzando le tue credenziali federate
    sts_client = boto3.client('sts')
    response = sts_client.get_session_token(DurationSeconds=3600, Policy='arn:aws:iam::597682427518:policy/allfortrip')

    # Ottieni le credenziali temporanee
    credentials = response['Credentials']
    access_key = credentials['AccessKeyId']
    secret_key = credentials['SecretAccessKey']
    session_token = credentials['SessionToken']
    region_name = 'us-east-1'
    account_id = 597682427518

    # Inizializza Boto3 con le credenziali temporanee
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        aws_session_token=session_token,
        region_name=region_name,
        account_id=account_id
    )

    return session, access_key, secret_key, session_token
