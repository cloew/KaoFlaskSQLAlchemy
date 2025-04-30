
class RecordValueProvider:
    """ Represents a wrapper to extract the proper values dictionary for a record from the JSON """
    
    def __init__(self, jsonColumnMap={}):
        """ Initialize the Provider with the map of values """
        self.jsonColumnMap = jsonColumnMap
        
    def getRecordValues(self, json):
        """ Return the record values """
        values = {}
        for key in json:
            if key in self.jsonColumnMap:
                newKey, value = self.jsonColumnMap[key](json[key])
                values[newKey] = value
            else:
                values[key] = json[key]
        return values