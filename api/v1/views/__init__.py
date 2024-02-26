#!/usr/bin/python3
# initialise package

from flask import Blueprint
from api.v1.views.states import init_state
from .index import *
from .cities import *
from .places_reviews import *
from .states import *
from api.v1.views.amenities import init_amenity
from api.v1.views.user import init_user

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
init_app(app_views)
init_state(app_views)
init_amenity(app_views)
init_user(app_views)
init_app(app_views)
init_cities(app_views)
init_review(app_views)
