from flask import Flask
from database.db import initialize_db
from flask_restful import Api
from resources.route import initialize_routes

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY']='myProject'
username = "test"
password = "test"
app.config['MONGODB_SETTINGS'] ={
    'host':'mongodb://'+username+':'+password+'@182.252.132.39/test'#+ '/?authSource=admin'
}
initialize_db(app)
initialize_routes(api)

if __name__=="__main__":
    app.run(debug=True)