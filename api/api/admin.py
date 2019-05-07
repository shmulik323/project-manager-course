from flask import Blueprint, current_app
from .models import db, User, Pdf

bp = Blueprint('bp', __name__)
