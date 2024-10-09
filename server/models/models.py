#models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from .novelty_model import *
from .obviousness_model import *
from .patent_model import *
from .prior_art_model import *
from .user_model import *
from .utility_model import *


db = SQLAlchemy()

