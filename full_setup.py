import boto3
from decimal import *

# Set up dinamodb client with boto3
client = boto3.client('dynamodb', region_name='eu-central-1')

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
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        }
    )
    print("Table created successfully!")

except Exception as e:
    print("Error creating table:")
    print(e)

######################################

#### Insert landmarks in table #######

#Set up decimal precision
getcontext().prec = 6

#Set up boto3
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
table = dynamodb.Table('Landmarks')

#Recover landmarks
fd = open("landmarks.csv", "r")

lines = fd.readlines()

# Write multiple items with one requests with batch writer
with table.batch_writer() as batch:
    for i in range(1, len(lines)):
        splitted = lines[i].strip().split(", ")
        batch.put_item(Item={"Name": splitted[0], "ID": int(i-1), "Lat": Decimal(splitted[1]), "Long": Decimal(splitted[2]), "Fog1": Decimal(splitted[3]), "Fog2" : Decimal(splitted[4])})
        #print({"Name": splitted[0], "ID": int(i), "Lat": Decimal(splitted[1]), "Long": Decimal(splitted[2]) })

print("Item inserted successfuly!")

######################################
