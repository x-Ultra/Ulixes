import boto3
from decimal import *
from time import sleep

# Set up dinamodb client with boto3
client = boto3.client('dynamodb', region_name='eu-central-1')

#### Create Distances table #######

try:
    resp = client.create_table(
        TableName="Distances",
        
        #Primary key
        KeySchema=[
            {
                "AttributeName": "Start",
                "KeyType": "HASH"
            }, 
            {
                "AttributeName": "End",
                "KeyType": "RANGE"
            }
        ],

        # Primary key type
        AttributeDefinitions=[
            {
                "AttributeName": "Start",
                "AttributeType": "S"
            },
            {
                "AttributeName": "End",
                "AttributeType": "S"
            }
        ],

        # Rate of access
        ProvisionedThroughput={
            "ReadCapacityUnits": 3,
            "WriteCapacityUnits": 3
        }
    )
    print("Table created successfully!")

except Exception as e:
    print("Error creating table:")
    print(e)

######################################

print("Waiting for table to be ready...")
sleep(5)

#### Insert landmarks in table #######

#Set up decimal precision
getcontext().prec = 6

#Set up boto3
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
table = dynamodb.Table('Distances')

#Recover landmarks
fd = open("distancesDB.csv", "r")

lines = fd.readlines()

# Write multiple items with one requests with batch writer
with table.batch_writer() as batch:
    for i in range(1, 5):
        splitted = lines[i].strip().split(", ")
        batch.put_item(Item={"Start": splitted[0], "End": splitted[1], "Seconds": int(splitted[2]), "Transports": splitted[3], "Fog1": Decimal(splitted[4]), "Fog2" : Decimal(splitted[5])})
        #print({"Name": splitted[0], "ID": int(i), "Lat": Decimal(splitted[1]), "Long": Decimal(splitted[2]) })
        if (i%100 == 0):
            print(i, " items inserted!")
print("Distances are online!")

######################################

