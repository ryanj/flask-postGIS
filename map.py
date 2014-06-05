import os
from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort
import pg
import json

app = Flask(__name__)
app.config.from_pyfile('map.cfg')
print dir(app.config)

db = pg.connect(app.config['APP_NAME'], \
     app.config['PG_DB_HOST'], \
     app.config['PG_DB_PORT'], \
     None, None, \
     app.config['PG_DB_USERNAME'], \
     app.config['PG_DB_PASSWORD'] )

@app.route('/')
def index():
    return render_template('index.html')

#return all parks:
@app.route("/parks")
def parks():
    table_name = app.config['APP_NAME']
    #query the DB for all the parkpoints
    result = db.query('SELECT gid,name,ST_X(the_geom) as lon,ST_Y(the_geom) as lat FROM '+ table_name+";")

    #Now turn the results into valid JSON
    return str(json.dumps(list(result.dictresult())))

#bounding box (within?lat1=45.5&lon1=-82&lat2=46.5&lon2=-81)
@app.route("/parks/within")
def within():
    table_name = app.config['APP_NAME']
    #get the request parameters
    lat1 = str(request.args.get('lat1'))
    lon1 = str(request.args.get('lon1'))
    lat2 = str(request.args.get('lat2'))
    lon2 = str(request.args.get('lon2'))
    limit = 25

    #use the request parameters in the query
    result = db.query("SELECT gid,name,ST_X(the_geom) as lon,ST_Y(the_geom) as lat FROM "+table_name+" t WHERE ST_Intersects( \
        ST_MakeEnvelope("+lon1+", "+lat1+", "+lon2+", "+lat2+", 4326), t.the_geom) LIMIT "+str(limit)+";")

    #turn the results into valid JSON
    return str(json.dumps(list(result.dictresult())))

@app.route('/static/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

@app.route("/test")
def test():
    return "<strong>It's Alive!</strong>"

if __name__ == '__main__':
    app.run()
