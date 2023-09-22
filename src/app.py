"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": "Miembro con ID {} no encontrado".format(id)}), 404

@app.route('/member', methods=['POST'])
def add_member():
    try:
        request_data = request.get_json()
        # Verifica si el campo 'id' está presente en la solicitud
        if 'id' not in request_data:
            return jsonify({"error": "El campo 'id' es obligatorio"}), 400
        # Obtiene el valor del campo 'id' desde la solicitud
        member_id = request_data['id']
    # fill this method and update the return
        request_body = json.loads(request.data)
        jackson_family.add_member(request_body)
        return jsonify({"message": "Miembro agregado con éxito"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    # fill this method and update the return
    success = jackson_family.delete_member(id)
    if success:
        response_data = {"done": True}
        return jsonify(response_data), 200
    else:
        return jsonify({"error": "Miembro no encontrado"}), 404
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
