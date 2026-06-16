from fastapi import Depends, HTTPException
from taskflow.app.services.auth_service import get_current_user

def require_admin(current_user = Depends(get_current_user)):
    user = current_user.get("role_id")
    
    if user != "1":
        raise HTTPException(
            status_code=403,
            detail="admin access required"
        )
        
    return current_user