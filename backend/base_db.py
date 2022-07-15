from enum import Enum, EnumMeta
from dataclasses import dataclass
from typing import Any, List
import boto3

class _BaseEnumMeta(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True
    
class _BaseEnum(Enum, metaclass=_BaseEnumMeta):
    @classmethod
    def find_attribute(cls, value):
        return cls[value].name

class BaseData:
    '''Class to provide common parent type to dataclasses and for future uses'''
    pass

def enumclass(cls=None, /, *, DataClass: BaseData = None, partition_key: str = None, **kwargs):  
    def process(cls):
        data_fields = list(DataClass.__dataclass_fields__.keys())
        setattr(cls, 'Attribute', _BaseEnum('Attribute', [(field.upper(), field) for field in data_fields]))
        
        if partition_key[0] in cls.Attribute:
            cls.partition_key = partition_key
        else:
            raise ValueError(f"{partition_key[0]} is not an attribute of the table")
        
        for attribute in kwargs:
            if attribute in data_fields:
                setattr(cls, attribute.capitalize(), _BaseEnum(attribute.capitalize(), [(element.upper(), element.upper()) for element in kwargs[attribute]]))
            else:
                del cls
                raise ValueError(f"{attribute} is not an attribute of the table")
        return cls
    
    if cls is not None or DataClass is None:
        raise Exception("Please provide a corresponding dataclass")
    return process

def changevar(cls=None, /, *, DataClass=None, EnumClass=None):
    def process(cls):
        cls.DataClass = DataClass
        cls.EnumClass = EnumClass
        return cls
    
    if cls is not None:
        raise Exception("Please provide the corresponding data and enum classes")
    return process


class BaseDDBUtil:
    DataClass = None
    EnumClass = None
    
    """
    Data access object for DynamoDB tables
    """    
    def __init__(self, table_name: str, region: str, table=None):
        self.table_name = table_name
        #self.dynamodb = boto3.resource('dynamodb', region)
        #self.table = table if table else boto3.resource('dynamodb', region).Table(self.table_name)
        
    def create_table(self, read_capacity_units: int = 10, write_capacity_units: int = 10) -> None:
        """
        Helper function to create Dynamo DB table if it doesn't exist in AWS
        """
        table = self.dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=[
                {
                    'AttributeName': self.partition_key[0],
                    'KeyType': 'HASH'  # Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': self.partition_key[0],
                    # AttributeType defines the data type. 'S' is string type and 'N' is number type
                    'AttributeType': self.partition_key[1]
                }
            ],
            ProvisionedThroughput={
                # ReadCapacityUnits set to 10 strongly consistent reads per second
                'ReadCapacityUnits': read_capacity_units,
                'WriteCapacityUnits': write_capacity_units  # WriteCapacityUnits set to 10 writes per second
            }
        )
        self.table = table
        
    def param_checker(self, operation: str, **kwargs):
        kwargs = kwargs.items()
        
        for attribute, value in kwargs:
            if attribute == 'record_data':
                if attribute is not None:
                    if type(value) is not self.DataClass:
                        raise ValueError(f"Could not {operation} record with {attribute} not of correct type")
                    if len(kwargs) > 1:
                        raise ValueError(f"Cannot provide other attributes if {attribute} is provided")
                elif len(kwargs) == 1:
                    raise ValueError(f"Could not {operation} record with missing attributes")
                pass
            elif attribute == 'partition_id':
                attribute = self.EnumClass.partition_key[0]
                
            if attribute not in self.EnumClass.Attribute:
                raise ValueError(f"Attribute not found in table {self.table_name}")
            elif value is None:
                raise ValueError(f"Could not {operation} record with {attribute}: None")
            elif type(value) is not self.DataClass.__dataclass_fields__[attribute].type:
                raise ValueError(f"Could not {operation} record with {attribute} not of correct type")
            elif getattr(self.EnumClass, attribute, None) is not None and value not in getattr(self.EnumClass, attribute):
                raise ValueError(f"Could not {operation} record with invalid {attribute}: {value}")
            
                

# Usage
if __name__ == '__main__':
    @dataclass
    class StatusData(BaseData):
        request_id: str
        status: str 
        timestamp: str

    @enumclass(DataClass=StatusData, partition_key=['request_id', 'S'], status=['started', 'in_progress', 'success', 'failed'])
    class StatusEnums:
        pass
    
    #print(StatusEnums)
    #print(StatusEnums.Attribute)
    #print(StatusEnums.Status)
    #print(StatusEnums.Status.IN_PROGRESS.value)
    #print('IN_PROGRESS' in StatusEnums.Status)
    
    @changevar(DataClass=StatusData, EnumClass=StatusEnums)
    class StatusDDBUtil(BaseDDBUtil):
        pass
    
    a = StatusData(1, 2, 3)
    print(dir(a))
    print(type(a).__name__)
    print(type(a) is StatusData)