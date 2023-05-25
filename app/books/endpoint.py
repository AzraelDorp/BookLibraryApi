# TODO: clean up doc
from flask_restx import Namespace, Resource


api = Namespace("books", description="")

# plural for many
@api.route("")
class PeopleAPI(Resource):
    @api.doc(responses={"200": "OK"})
    def get(self):
        '''Returns all people with filters'''
        return {"success", 200}
        
