import boto3
from decimal import *
from time import sleep
from helpers.configManager import cred_get

# Set up dinamodb client with boto3
client = boto3.client('dynamodb', region_name='eu-central-1', 
    aws_access_key_id=cred_get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=cred_get("AWS_SECRET_ACCESS_KEY"))

#### Create Landmarks table #######

try:
    resp = client.create_table(
        TableName="Landmarks",
        
        #Primary key
        KeySchema=[
            {
                "AttributeName": "Name",
                "KeyType": "HASH"
            }
        ],

        # Primary key type
        AttributeDefinitions=[
            {
                "AttributeName": "Name",
                "AttributeType": "S"
            }
        ],

        # Rate of access
        ProvisionedThroughput={
            "ReadCapacityUnits": 10,
            "WriteCapacityUnits": 10
        }
    )
    print("Landmarks table created successfully!")

except Exception as e:
    print("Error creating table:")
    print(e)

######################################

print("Waiting for landmarks table to be ready...")
sleep(5)

#### Insert landmarks in table #######

#Set up decimal precision
getcontext().prec = 6

#Set up boto3
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1', 
    aws_access_key_id=cred_get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=cred_get("AWS_SECRET_ACCESS_KEY"))
table = dynamodb.Table('Landmarks')

#Recover landmarks
fd = open("landmarksComplete.csv", "r")

lines = fd.readlines()

# Write multiple items with one requests with batch writer
with table.batch_writer() as batch:
    for i in range(1, len(lines)):
        splitted = lines[i].strip().split(", ")
        batch.put_item(Item={"Name": splitted[0], "ID": int(i-1), "Lat": Decimal(splitted[1]), "Long": Decimal(splitted[2]), "Fog1": Decimal(splitted[3]), "Fog2" : Decimal(splitted[4]), "PictureUrl" : splitted[5], "Description": "".join(splitted[6:])})
        #print({"Name": splitted[0], "ID": int(i), "Lat": Decimal(splitted[1]), "Long": Decimal(splitted[2]) })

print("Landamrks are online!")

######################################

# Set up dinamodb client with boto3
client = boto3.client('dynamodb', region_name='eu-central-1', 
    aws_access_key_id=cred_get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=cred_get("AWS_SECRET_ACCESS_KEY"))
#### Create Distances table #######

try:
    resp = client.create_table(
        TableName="Distances",
        
        #Primary key
        KeySchema=[
            {
                "AttributeName": "ID",
                "KeyType": "HASH"
            }
        ],

        # Primary key type
        AttributeDefinitions=[
            {
                "AttributeName": "ID",
                "AttributeType": "N"
            }
        ],

        # Rate of access
        ProvisionedThroughput={
            "ReadCapacityUnits": 30,
            "WriteCapacityUnits": 30
        }
    )
    print("Disntaces table created successfully!")

except Exception as e:
    print("Error creating table:")
    print(e)

######################################

print("Waiting for distances table to be ready...")
sleep(5)

#### Insert distances in table #######

#Set up decimal precision
getcontext().prec = 6

#Set up boto3
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1', 
    aws_access_key_id=cred_get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=cred_get("AWS_SECRET_ACCESS_KEY"))
table = dynamodb.Table('Distances')

#Recover landmarks
fd = open("distancesDB.csv", "r")

lines = fd.readlines()

# Write multiple items with one requests with batch writer
with table.batch_writer() as batch:
    for i in range(1, len(lines)):
        splitted = lines[i].strip().split(", ")
        batch.put_item(Item={"ID": i, "Start": splitted[0], "End": splitted[1], "Seconds": int(splitted[2]), "Transport": splitted[3], "Fog1": Decimal(splitted[4]), "Fog2" : Decimal(splitted[5])})
        #print({"Name": splitted[0], "ID": int(i), "Lat": Decimal(splitted[1]), "Long": Decimal(splitted[2]) })
        if (i%100 == 0):
            print(i, " items inserted!")
print("Distances are online!")

######################################
