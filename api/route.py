from api import app, api
from api.api_classes import Users, Cats, FavoriteList


# API ROUTES
api.add_resource(Users, '/user')
api.add_resource(Cats, '/cat')
api.add_resource(FavoriteList, '/list')


# END OF API ROUTES
@app.route('/')
def index():
    return "The API endpoints are <a href='http://api.spibes.com/api/user'>http://api.spibes.com/api/user</a>" \
           " <a href='http://api.spibes.com/api/cat'>http://api.spibes.com/api/cat</a> and " \
           "<a href='http://api.spibes.com/api/list'>http://api.spibes.com/api/list</a> for the User," \
           " Category and FavoriteList respectively."
