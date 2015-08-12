from .record_value_provider import RecordValueProvider
from ..database import db

from kao_flask.controllers.json_controller import JSONController
from smart_defaults import smart_defaults, EvenIfNone

class CreateController(JSONController):
    """ Controller to create a new record for a particular model """
    
    @smart_defaults
    def __init__(self, modelCls, toJson, routeParams={}, recordValueProvider=EvenIfNone(RecordValueProvider()), decorators=[]):
        """ Initialize the Create Controller """
        JSONController.__init__(self, decorators=decorators)
        self.modelCls = modelCls
        self.toJson = toJson
        self.routeParams = routeParams
        self.recordValueProvider = recordValueProvider
    
    def performWithJSON(self, **kwargs):
        """ Convert the records to JSON """
        json = kwargs['json']
        record = self.create(json, kwargs=kwargs)
        return {"record":self.toJson(record, **kwargs)}

    def create(self, json, kwargs={}):
        """ Create the record """
        recordValues = {self.routeParams[routeParam]:kwargs[routeParam] for routeParam in self.routeParams}
        providedRecordValues = self.recordValueProvider.getRecordValues(json)
        recordValues.update(providedRecordValues)
        record = self.modelCls(**recordValues)
        
        db.session.add(record)
        db.session.commit()
        return record