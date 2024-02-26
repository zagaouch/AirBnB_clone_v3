# In api/v1/views/users.py


from flask import jsonify, abort, request
from models import storage
from models.user import User


def init_user(app_views):
    @app_views.route('/users', methods=['GET'], strict_slashes=False)
    def get_users():
        users = storage.all("User")
        return jsonify([user.to_dict() for user in users.values()])

    @app_views.route('/users/<user_id>', methods=['GET'],
                     strict_slashes=False)
    def get_user(user_id):
        user = storage.get("User", user_id)
        if user is None:
            abort(404)
        return jsonify(user.to_dict())

    @app_views.route('/users/<user_id>', methods=['DELETE'],
                     strict_slashes=False)
    def delete_user(user_id):
        user = storage.get("User", user_id)
        if user is None:
            abort(404)
        storage.delete(user)
        storage.save()
        return jsonify({}), 200

    @app_views.route('/users', methods=['POST'], strict_slashes=False)
    def create_user():
        if not request.is_json:
            return jsonify({"error": "Not a JSON"}), 400
        data = request.get_json()
        if data is None or 'email' not in data:
            return jsonify({"error": "Missing email"}), 400
        if 'password' not in data:
            return jsonify({"error": "Missing password"}), 400
        user = User(**data)
        user.save()
        return jsonify(user.to_dict()), 201

    @app_views.route('/users/<user_id>', methods=['PUT'],
                     strict_slashes=False)
    def update_user(user_id):
        user = storage.get("User", user_id)
        if user is None:
            abort(404)
        if not request.is_json:
            return jsonify({"error": "Not a JSON"}), 400
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
