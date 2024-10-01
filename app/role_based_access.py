from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from typing import List, Optional


def check_access(current_data,data):
    if current_data.user_role=="admin":
        print(current_data.user_role,"This is admin account")
        return
    
    elif data is not None and current_data.org_id==data.org_id and current_data.user_role=="manager":
        print("This is manager acccount")
        return
    elif data is not None and current_data.org_id==data.org_id and current_data.user_role=="viewer":
        print("Viewer login")
        return
    else:
        return JSONResponse(status_code=403, content={"detail": "You do not have permission to access resource"})