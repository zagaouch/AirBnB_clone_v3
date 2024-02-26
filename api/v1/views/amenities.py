# In api/v1/views/amenities.py


from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


def init_amenity(app_views):
    @app_views.route('/amenities', methods=['GET'], strict_slashes=False)
    def get_amenities():
        amenities = storage.all("Amenity")
        return jsonify([amenity.to_dict() for amenity in amenities.values()])

    @app_views.route('/amenities/<amenity_id>', methods=['GET'])
    def get_amenity(amenity_id):
        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            abort(404)
        return jsonify(amenity.to_dict())

    @app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                     strict_slashes=False)
    def delete_amenity(amenity_id):
        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            abort(404)
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    @app_views.route('/amenities', methods=['POST'], strict_slashes=False)
    def create_amenity():
        if not request.is_json:
            return jsonify({"error": "Not a JSON"}), 400
        data = request.get_json()
        if data is None or 'name' not in data:
            return jsonify({"error": "Missing name"}), 400
        amenity = Amenity(**data)
        amenity.save()
        return jsonify(amenity.to_dict()), 201

    @app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                     strict_slashes=False)
    def update_amenity(amenity_id):
        amenity = storage.get("Amenity", amenity_id)
        if amenity is None:
            abort(404)
        if not request.is_json:
            return jsonify({"error": "Not a JSON"}), 400
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
