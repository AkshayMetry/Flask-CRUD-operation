from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017")
# db = client.lin_flask
db = client['flaskdb'] ## database name
CORS(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/users', methods=['POST', 'GET'])
def data():
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        username = body['username']
        emailId = body['emailId'] 
        age = body['age']
        # db.users.insert_one({
        db['users'].insert_one({
            
            "username":username,
            "emailId":emailId,
            "age": age
        })
        return jsonify({
            'status': 'Data is posted to MongoDB!',
            'username':username,
            'emailId':emailId,
            'age':age
        })

    # GET all data from database
    if request.method == 'GET':
        allData = db['users'].find()
        dataJson = []
        for data in allData:
            id = data['_id']
            username = data['username']
            emailId = data['emailId']
            age = data['age']

            dataDict = {
                'id': str(id),
                'username':username,
                'age':age,
                'emailId':emailId
            }
            dataJson.append(dataDict)
        print(dataJson)
        return jsonify(dataJson)
    
@app.route('/users/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):

    # GET a specific data by id
    if request.method == 'GET':
        data = db['users'].find_one({'_id': ObjectId(id)})
        id = data['_id']
        username = data['username']
        age = data['age']
        emailId = data['emailId']
        dataDict = {
            'id': str(id),
            'username': username,
            'age':age,
            'emailId':emailId
        }
        print(dataDict)
        return jsonify(dataDict)
    

    # DELETE a data
    if request.method == 'DELETE':
        db['users'].delete_many({'_id': ObjectId(id)})
        print('\n # Deletion successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is deleted!'})
    
    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        username = body['username']
        age = body['age']
        emailId = body['emailId']
 
        db['users'].update_one(
            {'_id': ObjectId(id)},
            {
                "$set": {
                    "username":username,
                    'age':age,
                    "emailId": emailId
                }
            }
        )
 
        print('\n # Update successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is updated!'})
 

if __name__ == '__main__':
    app.debug = True
    app.run()