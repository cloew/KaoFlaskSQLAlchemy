from .database import db

class SqlAlchemyExtension:
    """ Represetns an extension to setup the Server for SQLAlchemy integration """
    
    def initialize(self, server):
        """ Initialize the Server with the extension """
        db.init_app(server.app)
        server.db = db