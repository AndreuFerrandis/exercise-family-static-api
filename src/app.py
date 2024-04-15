"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    if members:
        return jsonify(members), 200
    else:
        raise APIException("Members not found", status_code=404)

@app.route('/member/<int:member_id>', methods=['GET'])
def handle_hello(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        raise APIException("Member not found", status_code=404)

@app.route('/member', methods=['POST'])
def add_member():
    request_data = request.json
    if not request_data:
        raise APIException("Request body must be JSON", status_code=400)
    new_member = jackson_family.add_member(request_data)
    return jsonify(new_member), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    result = jackson_family.delete_member(member_id)
    if result["done"]:
        return jsonify({"done": True}), 200
    else:
        raise APIException("Member not found", status_code=404)
    
if __name__ == '__main__':
    app.run(debug=True)