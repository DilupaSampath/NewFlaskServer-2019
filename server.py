from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['MONGO_DBNAME'] = 'DataBaseName'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/DataBaseName'

mongo = PyMongo(app)


@app.route('/simple-post/', methods=['POST'])
def simplePost():
    if request.method=='POST':  
        data = request.get_json()
        print(data)
        mongo.db.tableName.insert_one(data)
        return jsonify({'ok': True, 'message': 'created successfully!'})


@app.route('/simple-get/', methods=['GET'])
def simpleGet():
  tableModel = mongo.db.tableName
  output = []
  for s in tableModel.find():
    output.append({'id':s['id'],'NIC':s['NIC'],'name' : s['name']})
  return jsonify(output)

@app.route('/simple-delete/', methods=['DELETE'])
def simpleDelete():
    data = request.get_json()
    db_response = mongo.db.tableName.delete_one({'id': data['id']})
    if db_response.deleted_count == 1:
        response = {'ok': True, 'message': 'record deleted'}
    else:
        response = {'ok': True, 'message': 'no record found'}
    return jsonify(response), 200
@app.route('/simple-patch/', methods=['PATCH'])
def simpleUpdate():
    data1 = request.get_json()
    data = mongo.db.tableName
    result = mongo.db.tableName.update({"id":data1['id']},{'$set':{'name':data1['name']}})
    response = {'ok': True, 'message': 'record updated'}
    print data.find_one({'ID':100})
    return jsonify(response), 200


if __name__ == '__main__':  
    app.run(host= '0.0.0.0')
    
