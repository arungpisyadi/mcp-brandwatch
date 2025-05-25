from typing import Any, Dict
from fastapi import Depends, HTTPException
from app.interfaces.base import IController
from app.presenters.user_presenter import UserPresenter
from app.models.user import User
from app.core.security import get_current_user

class UserController(IController):
    def __init__(self, presenter: UserPresenter):
        self.presenter = presenter

    async def handle_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle request for user operations
        """
        action = request_data.get("action")
        
        if action == "get_current_user":
            current_user = await get_current_user()
            return self.presenter.transform_data(current_user)
        
        raise HTTPException(status_code=400, detail="Invalid action") 