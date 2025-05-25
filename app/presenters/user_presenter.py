from typing import Any, Dict
from app.interfaces.base import IPresenter
from app.models.user import User

class UserPresenter(IPresenter):
    def transform_data(self, data: User) -> Dict[str, Any]:
        """
        Transform user data for API response
        """
        return {
            "id": str(data.id),
            "email": data.email,
            "username": data.username,
            "is_active": data.is_active,
            "created_at": data.created_at.isoformat() if data.created_at else None,
            "updated_at": data.updated_at.isoformat() if data.updated_at else None
        }

    def transform_list(self, users: list[User]) -> list[Dict[str, Any]]:
        """
        Transform list of user data for API response
        """
        return [self.transform_data(user) for user in users] 