from flask import Flask, jsonify, request
from bson.objectid import ObjectId
from application import app, mongo
from application.locus import Locus, LocusSchema, ValidationError

# Setup MongoDB connection
db = mongo.db

# Default action is to get all entries, but can also specify for a certain entry
@ app.route('/locus', methods=['GET'])
def get_locus():
        conditions = request.args
        if conditions:
            try: 
                filter = {}
                name, type, priority = conditions.get('name'), conditions.get('type'), conditions.get('priority')
                place_id, address, url = conditions.get('place_id'), conditions.get('address'), conditions.get('url')

                if name is not None: filter['name'] = {'$in': [name]}
                if type is not None: filter['type'] = {'$in': [type]}
                if priority is not None: filter['priority'] = {'$gte': int(priority)}
                if place_id is not None: filter['place_id'] = {'$in': [place_id]}
                if address is not None: filter['address'] = {'$in': [address]}
                if url is not None: filter['url'] = {'$in': [url]}
                
                locus = LocusSchema(many=True).dump(db.places.find(filter))
                return jsonify(locus)
            except ValidationError as e:
                return jsonify({'error': e.messages}), 400
        else:
            locus = LocusSchema(many=True).dump(db.places.find())
            return jsonify(locus)



# Check if place ID exists previously, if not it inserts into DB 
@app.route('/locus', methods=['POST'])
def add_locus():
    try:
        _json = LocusSchema().load(request.get_json())
        
        place_id = _json['place_id']
        if db.places.find_one({'place_id': place_id}):
            return jsonify({'error': 'Location with the same ID already exists'}), 409

        id = db.places.insert_one(_json)
        return jsonify({'message': 'Location created successfully'}), 201
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400



# Applies only to one ID to get, delete or update entry
@app.route('/locus/<id>', methods=['GET', 'DELETE', 'PUT'])
def one_locus(id):
    # Get only one entry based on ID provided
    if request.method == 'GET':
        locus = LocusSchema().dump(db.places.find_one({'_id': ObjectId(id)}))       
        return jsonify(locus)
    
    # Update an entry based on ID provided and ensures duplicate place_ID doesnt get overwritten
    elif request.method == 'PUT':
        _json = LocusSchema().load(request.get_json())

        place_id = _json['place_id']
        prev_place_id = db.places.find_one({'place_id': place_id})
        if prev_place_id and str(prev_place_id['_id']) != str(id):
            return jsonify({'error': 'Location with the same ID already exists'}), 409

        result = db.places.update_one({'_id': ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)}, {'$set': _json})
        if result.modified_count:
            return jsonify({'message': 'Location updated successfully'}), 202
        else:
            return jsonify({'message': 'Location not found'}), 404

    # Delete an entry based on ID provided
    elif request.method == 'DELETE':
        db.places.delete_one({'_id': ObjectId(id)})
        return jsonify({'message': 'Location deleted successfully!'}), 200
        
    else:
        return not_found()



# default route is to showcase all data available
@app.route('/locus')
def get_all_locus():
    locus = LocusSchema(many=True).dump(db.places.find())
    return jsonify(locus)
    


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == '__main__':
    app.run(debug=True)

