from .create_controller import CreateController
from .delete_controller import DeleteController
from .list_controller import ListController
from .record_controller import RecordController
from .update_controller import UpdateController

from .record_value_provider import RecordValueProvider

from kao_flask.endpoint import Endpoint

class CrudEndpoints:
    """ Represents the standard CRUD Endpoints for a particualr model class """
    
    def __init__(self, rootUrl, modelCls, toJson, routeParams={}, jsonColumnMap={}, decorators=[]):
        """ Initialize with the root URL and the model class to wrap """
        recordValueProvider = RecordValueProvider(jsonColumnMap)
        self.listEndpoint = Endpoint(rootUrl, get=ListController(modelCls, toJson, routeParams=routeParams, decorators=decorators), 
                                              post=CreateController(modelCls, toJson, routeParams=routeParams, recordValueProvider=recordValueProvider, decorators=decorators))
        self.recordEndpoint = Endpoint(rootUrl+'/<int:id>', get=RecordController(modelCls, toJson, decorators=decorators), 
                                                            put=UpdateController(modelCls, toJson, recordValueProvider=recordValueProvider, decorators=decorators), 
                                                            delete=DeleteController(modelCls, decorators=decorators))
        
    @property
    def endpoints(self):
        """ Return the endpoints """
        return [self.listEndpoint, self.recordEndpoint]