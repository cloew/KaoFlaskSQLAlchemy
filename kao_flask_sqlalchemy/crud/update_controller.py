from .record_value_provider import RecordValueProvider
from ..database import db

from kao_flask.controllers.json_controller import JSONController

class UpdateController(JSONController):
    """ Controller to update a record for a particular model """
    
    def __init__(self, modelCls, toJson, recordValueProvider=None, decorators=[]):
        """ Initialize the Update Controller """
        JSONController.__init__(self, decorators=decorators)
        self.modelCls = modelCls
        self.toJson = toJson
        self.recordValueProvider = recordValueProvider or RecordValueProvider()
    
    def performWithJSON(self, id, **kwargs):
        """ Remove the record """
        json = kwargs['json']
        record = self.update(id, json)
        return {"record":self.toJson(record, **kwargs)}
        
    def update(self, id, json):
        """ Update the record """
        record = self.modelCls.query.filter(self.modelCls.id==id).first()
        recordValues = self.recordValueProvider.getRecordValues(json)
        for key in recordValues:
            setattr(record, key, recordValues[key])
            
        db.session.add(record)
        db.session.commit()
        return record