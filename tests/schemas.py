from jsonschema import validate
import json


get_pingout_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",  
  "type": "object",
    "properties": {
      "pingout": { 
          "type": "object",
          "properties":{
              "pings":{
                  "type":"array",
                  "properties":{
                      "count": {"type": "number"},
                      "date": {"type": "string", "format": "date"},
                  }
              },
              "uuid": {"type": "string"}
          },
          "required": ["pings", "uuid"]
      }
    },
  "required": ["pingout"]
}

get_wrong_pingout_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",  
  "type": "object",
    "properties": {
      "errors": { "type": "string" }
    },
  "required": ["errors"]
}

create_file_ping = {
  "$schema": "http://json-schema.org/draft-04/schema#",  
  "type": "object",
    "properties": {
      "message": { "type": "string" },
      "url": {"type": "string"}
    },
  "required": ["message", "url"]
}

failure_create_file_ping = {
  "$schema": "http://json-schema.org/draft-04/schema#",  
  "type": "object",
    "properties": {
      "error": { "type": "string" }
    },
  "required": ["error"]
}

def assert_valid_schema(data, schema):
    """ Checks whether the given data matches the schema """    
    return validate(data, schema)