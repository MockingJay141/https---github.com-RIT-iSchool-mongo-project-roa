from flask import Flask, render_template, request, jsonify, send_file
from bson import ObjectId
import pymongo
import json
import re
from gridfs import GridFS
from io import BytesIO

app = Flask(__name__)

# MongoDB connection settings
mongo_host = 'localhost'
mongo_port = 27017
mongo_db = 'Mongo_Project'
mongo_collection = 'Tweets'

def serialize(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.json['query']
    latitude = request.json['latitude']
    longitude = request.json['longitude']

    # Connect to MongoDB
    client = pymongo.MongoClient(mongo_host, mongo_port)
    db = client[mongo_db]
    collection = db[mongo_collection]

    # Create the query conditions based on latitude and longitude
    conditions = {'text': re.compile(query)}
    if latitude and longitude:
        conditions['latitude'] = float(latitude)
        conditions['longitude'] = float(longitude)

    # Execute the query
    results = list(collection.find(conditions, {'_id': 1, 'user_location': 1}))

    # Retrieve the user_location from the _id of the results
    user_locations = [str(result['user_location']).split('-')[0] for result in results]

    # Connect to GridFS
    fs = GridFS(db)

    # Find the image filenames associated with the user_location
    filenames = []
    for user_location in user_locations:
        file_cursor = fs.find({'filename': {'$regex': f'{user_location}-\d+'}})
        filenames += [file.filename for file in file_cursor]

    # Close the MongoDB connection
    client.close()

    # Add image filenames to the results
    for i, result in enumerate(results):
        result['image_filenames'] = [filename for filename in filenames if filename.startswith(user_locations[i])]

    return json.dumps(results, default=serialize)

@app.route('/document')
def get_document():
    document_id = request.args.get('id')

    # Connect to MongoDB
    client = pymongo.MongoClient(mongo_host, mongo_port)
    db = client[mongo_db]
    collection = db[mongo_collection]

    # Retrieve the document
    document = collection.find_one({'_id': ObjectId(document_id)}, {'date': 0})

    # Close the MongoDB connection
    client.close()

    return json.dumps(document, default=serialize)

@app.route('/images/<filename>')
def get_image(filename):
    # Connect to MongoDB
    client = pymongo.MongoClient(mongo_host, mongo_port)
    db = client[mongo_db]

    # Access the GridFS collection
    fs = GridFS(db)

    # Retrieve the image file from GridFS
    image_file = fs.find_one({'filename': filename})

    # Read the image data from GridFS
    image_data = image_file.read()

    # Create a BytesIO object to hold the image data
    image_stream = BytesIO(image_data)

    # Close the MongoDB connection
    client.close()

    return send_file(image_stream, mimetype='image/jpeg')


@app.route('/add-comment', methods=['POST'])
def add_comment():
    data = request.get_json()
    client = pymongo.MongoClient(mongo_host, mongo_port)
    db = client[mongo_db]
    collection = db[mongo_collection]
    id = data['id']
    comment = data['comment']
    print(id)

    # Update the document with the comment
    result = collection.update_one({'_id': ObjectId(id)}, {'$push': {'comments': comment}})

    if result.modified_count > 0:
        response = {'success': True}
    else:
        response = {'success': False}

    return jsonify(response)


if __name__ == '__main__':
    app.run()
