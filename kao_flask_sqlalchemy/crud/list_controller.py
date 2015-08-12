from kao_flask.controllers.json_controller import JSONController

class ListController(JSONController):
    """ Controller to return the list of all records for a particular model """
    
    def __init__(self, modelCls, toJson, routeParams={}, decorators=[]):
        """ Initialize the List Controller """
        JSONController.__init__(self, decorators=decorators)
        self.modelCls = modelCls
        self.toJson = toJson
        self.routeParams = routeParams
    
    def performWithJSON(self, *args, **kwargs):
        """ Convert the records to JSON """
        json = kwargs['json']
        
        query = self.modelCls.query.filter_by(**{self.routeParams[routeParam]:kwargs[routeParam] for routeParam in self.routeParams})
        return {"records":self.toJson(query.all(), **kwargs)}