#!/usr/bin/python3
# routes for state


from flask import jsonify, request, abort
from models import storage
from modesl.state import State


def init_state(app_views):
    @app_views.route('/states', methods=['GET'], strict_slashes=False)
    def get_states():
        states = storage.all("State")
        return jsonify([state.to_dict() for state in states.values()])

    @app_views.route('/states/<state_id>', methods=['GET'],
                     strict_slashes=False)
    def get_state(state_id):
        state = storage.get("State", state_id)
        if state is None:
            abort(404)
        return jsonify(state.to_dict())

    @app_views.route('/states/<state_id>', methods=['DELETE'],
                     strict_slashes=False)
    def delete_state(state_id):
        state = storage.get("State", state_id)
        if state is None:
            abort(404)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200

    @app_views.route('/states', methods=['POST'], strict_slashes=False)
    def create_state():
        if not request.is_json:
            return jsonify({"error": "Not a JSON"}), 400
        data = request.get_json()
        if data is None or 'name' not in data:
            return jsonify({"error": "Missing name"}), 400
        state = State(**data)
        state.save()
        return jsonify(state.to_dict()), 201

    @app_views.route('/states/<state_id>', methods=['PUT'],
                     strict_slashes=False)
    def put_state(state_id):
        state = storage.get("State", state_id)
        if not request.is_json:
            return jsonify({"error": "Not a JSON"}), 400
        if state is None:
            abort(404)
        data = request.get_json()
        for key, value in data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
