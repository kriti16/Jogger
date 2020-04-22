from flask_jwt_extended import jwt_required, get_jwt_identity

from .roles import ROLES
from app.database.models import User

@jwt_required
def min_access_level(self, role):
	current_user = User.query.get(get_jwt_identity())
	return current_user.role>=role