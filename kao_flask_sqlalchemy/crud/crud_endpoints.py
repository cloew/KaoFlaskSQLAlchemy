from .record_value_provider import RecordValueProvider
from ..database import db

from kao_flask import Endpoint, with_json

def apply_decorators(fn, decorators):
    """ Wraps the given function in the list of decorators """
    for decorator in reversed(decorators):
        fn = decorator(fn)
    return fn

class CrudEndpoints:
    """ Represents the standard CRUD Endpoints for a particular model class """
    
    def __init__(self, rootUrl, modelCls, toJson, routeParams={}, jsonColumnMap={}, decorators=[]):
        """ Initialize with the root URL and the model class to wrap """
        self.rootUrl = rootUrl
        self.modelCls = modelCls
        self.toJson = toJson
        self.routeParams = routeParams
        self.decorators = decorators
        
        self.recordValueProvider = RecordValueProvider(jsonColumnMap)

    @with_json
    def list(self, *, json, **kwargs):
        """ List the records for the model """        
        query = self.modelCls.query.filter_by(**{self.routeParams[routeParam]:kwargs[routeParam] for routeParam in self.routeParams})
        return {"records":self.toJson(query.all(), **kwargs)}
        
    @with_json
    def create(self, *, json, **kwargs):
        """ Create an entry for the model """
        recordValues = {self.routeParams[routeParam]:kwargs[routeParam] for routeParam in self.routeParams}
        providedRecordValues = self.recordValueProvider.getRecordValues(json)
        recordValues.update(providedRecordValues)
        record = self.modelCls(**recordValues)
        
        db.session.add(record)
        db.session.commit()
        return {"record":self.toJson(record, **kwargs)}
        
    @with_json
    def read(self, *, id, json, **kwargs):
        """ Read an entry for the model """
        return {"record":self.toJson(self.modelCls.query.filter(self.modelCls.id==id).first(), **kwargs)}
        
    @with_json
    def update(self, *, id, json, **kwargs):
        """ Update an entry for the model """
        record = self.modelCls.query.filter(self.modelCls.id==id).first()
        recordValues = self.recordValueProvider.getRecordValues(json)
        for key in recordValues:
            setattr(record, key, recordValues[key])
            
        db.session.add(record)
        db.session.commit()
        return {"record":self.toJson(record, **kwargs)}
        
    @with_json
    def delete(self, *, id, json, **kwargs):
        """ Delete an entry for the model """
        record = self.modelCls.query.filter(self.modelCls.id==id).first()
        db.session.delete(record)
        db.session.commit()
        return {}
        
    @property
    def endpoints(self):
        """ Return the endpoints """
        return [self.list_endpoint, self.record_endpoint]
        
    @property
    def list_endpoint(self):
        """ Return the endpoints """
        return Endpoint(self.rootUrl, get=self.with_decorators(self.list), post=self.with_decorators(self.create))
        
    @property
    def record_endpoint(self):
        """ Return the endpoints """
        return Endpoint(self.rootUrl+'/<int:id>', get=self.with_decorators(self.read), put=self.with_decorators(self.update), delete=self.with_decorators(self.delete))
    
    def with_decorators(self, fn):
      """ Return the fn with the decorators the class was instantiated with """
      return apply_decorators(fn, self.decorators)
        
    def register(self, app):
        """ Register the underlying routes """
        for endpoint in self.endpoints:
            endpoint.register(app)