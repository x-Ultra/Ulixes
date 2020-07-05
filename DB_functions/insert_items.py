import boto3
from decimal import *

#Set up decimal precision
getcontext().prec = 6

#Set up boto3
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
table = dynamodb.Table('Landmarks')

#Recover landmarks
fd = open("../landmarks.csv", "r")

lines = fd.readlines()

# The BatchWriteItem API allows us to write multiple items to a table in one request.
with table.batch_writer() as batch:
    for i in range(1, len(lines)):
        splitted = lines[i].strip().split(", ")
        batch.put_item(Item={"Name": splitted[0], "ID": int(i-1), "Lat": Decimal(splitted[1]), "Long": Decimal(splitted[2]) })
        #print({"Name": splitted[0], "ID": int(i), "Lat": Decimal(splitted[1]), "Long": Decimal(splitted[2]) })
        if (i % 10 == 0):
            print("Inserted ", i, " items")

print("Item inserted successfuly!")
