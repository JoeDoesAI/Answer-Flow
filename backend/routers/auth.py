import os
from fastapi import APIRouter,Request


auth_router = APIRouter()

ACCESS_CODE = os.getenv("ACCESS_CODE")

@auth_router.post("/verify-access")
async def verify_access(request: Request):
    # request.session.get("access_code")
    access_code = "FLOW56" #later change to the top

    if access_code == ACCESS_CODE:
        request.session["authorized"] = True
        #RedirectResponse("/home")

        return {"logedin":"access-granted"}