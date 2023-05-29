# all interactions with database
import boto3
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer
from botocore.exceptions import ClientError
from marshmallow import EXCLUDE

# write a class that will inilitize aws credentials
# and will have methods to interact with the database
class DatabaseModel:
    def __init__(self):
        self.client = boto3.client('dynamodb', region_name='us-east-1')
        self.resource = boto3.resource('dynamodb', region_name='us-east-1')
        self.serializer = TypeSerializer()
        self.deserializer = TypeDeserializer()

    # create a table with the given name
    # and the given attributes
    def createTable(self, tableName, attributes):
        # create table
        try:
            self.client.create_table(
                TableName=tableName,
                AttributeDefinitions=attributes,
                KeySchema=[
                    {
                        'AttributeName': attributes[0]['AttributeName'],
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': attributes[1]['AttributeName'],
                        'KeyType': 'RANGE'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            return True
        except Exception as e:
            print("Error creating table: ", e)
            return False

    # delete a table with the given name
    def deleteTable(self, tableName):
        # delete table
        try:
            self.client.delete_table(
                TableName=tableName
            )
            return True
        except Exception as e:
            print("Error deleting table: ", e)
            return False

    # get all tables in database
    def getTables(self):
        # get all tables
        try:
            tables = self.client.list_tables()['TableNames']
            return tables
        except Exception as e:
            print("Error getting tables: ", e)
            return None
    
    # get all items in a table
    def getAllItems(self, tableName):
        # get all items
        try:
            table = self.resource.Table(tableName)
            items = table.scan()['Items']
            return items
        except Exception as e:
            print("Error getting all items: ", e)
            return None

    # get an item with given primary key
    def getItemsWithKey(self, tableName, tableSchema, key):
        # get an item
        try:
            get_result = self.client.get_item(
                TableName=tableName,
                Key=key,
            )
        except Exception as e:
            print("Error getting item: ", e)
            return None
        else:
            if get_result.get("Item"):
                deserialised = {k: self.deserializer.deserialize(v) for k, v in get_result.get("Item").items()}
                return tableSchema.load(deserialised, unknown=EXCLUDE)
            else:
                return None

    # add an item to a table
    def addItem(self, tableName, tableSchema, item):
        # add an item
        try:
            response = self.client.put_item(
                TableName=tableName,
                Item={k: self.serializer.serialize(v) for k, v in tableSchema.dump(item).items() if v != ""}
            )
        except ClientError as err:
            raise err
        else:
            return response    
            
    # # add an item to a table
    # def addItem(self, tableName, item):
    #     # add an item
    #     try:
    #         table = self.resource.Table(tableName)
    #         table.put_item(Item=item)
    #         return True
    #     except Exception as e:
    #         print("Error adding item: ", e)
    #         return False
        
    # update an item in a table
    def updateItemByID(self, tableName, tableSchema, key, item):
        # update an item
        try:
            self.client.put_item(
                TableName=tableName,
                Item={k: self.serializer.serialize(v) for k, v in tableSchema.dump(item).items() if v != ""},
            )
            return True
        except Exception as e:
            print("Error updating item: ", e)
            return False

    # delete an item in a table
    def deleteItem(self, tableName, key):
        # delete an item
        try:
            table = self.resource.Table(tableName)
            table.delete_item(Key=key)
            return True
        except Exception as e:
            print("Error deleting item: ", e)
            return False

    # get all items with given primary key and sort key
    def getItemsWithKeysAndFilterAndLimit(self, tableName, key, sortKey, filterExpression, expressionAttributeValues, limit):
        # get all items
        try:
            table = self.resource.Table(tableName)
            items = table.query(
                KeyConditionExpression=key,
                FilterExpression=filterExpression,
                ExpressionAttributeValues=expressionAttributeValues,
                ScanIndexForward=False,
                Limit=limit)['Items']
            return items
        except Exception as e:
            print("Error getting items with keys and filter: ", e)
            return None
    
    # get all items with filter
    def getItemsWithFilter(self, tableName, filterExpression, expressionAttributeValues):
        # get all items with filter
        try:
            table = self.resource.Table(tableName)
            items = table.scan(
                FilterExpression=filterExpression,
                ExpressionAttributeValues=expressionAttributeValues)['Items']
            return items
        except Exception as e:
            print("Error getting items with filter: ", e)
            return None