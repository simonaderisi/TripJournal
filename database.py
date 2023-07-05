import boto3

# Crea un oggetto client per Amazon RDS
rds_client = boto3.client('rds')

# Specifica il nome del tuo cluster e l'identificatore dell'istanza
cluster_identifier = 'cluster-aurora'
instance_identifier = 'my-instance-identifier'

# Ottieni le informazioni sull'istanza di database
response = rds_client.describe_db_instances(
    DBInstanceIdentifier=instance_identifier,
    Filters=[
        {
            'Name': 'db-cluster-id',
            'Values': [cluster_identifier]
        },
    ]
)

# Estrai l'endpoint dell'istanza di database
endpoint = response['DBInstances'][0]['Endpoint']['Address']

# Configura le credenziali per la connessione al database
db_config = {
    'user': 'username',
    'password': 'password',
    'host': endpoint,
    'database': 'database_name'
}

# Ora puoi utilizzare il pacchetto psycopg2 o psycopg2-binary per connetterti al database
# e interagire con esso come descritto in precedenza
