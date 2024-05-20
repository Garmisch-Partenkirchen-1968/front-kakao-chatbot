from fastapi import APIRouter, Depends, HTTPException, Request
from src.repo.backend_api import get_backend_projects, verify_login
from src.login.session_manager import create_session, get_user_session
from src.response.kakao_response import create_kakao_response

router = APIRouter()

@router.post("/projects")
async def get_projects(user_session: dict = Depends(get_user_session)):
    try:
        projects = await get_backend_projects(user_session['username'], user_session['password'])
        response = create_kakao_response(
            outputs=[{"simpleText": {"text": f"ID: {proj.id}, Title: {proj.title}"}} for proj in projects],
            quick_replies=[{"label": "More projects", "action": "message", "messageText": "Show more projects"}]
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(request: Request):
    try:
        body = await request.json()
        user_info = body["action"]["params"]["userInfo"]
        kakaoId = body["userRequest"]["user"]["id"]

        if '@' not in user_info:
            raise HTTPException(status_code=400, detail="Invalid format for userInfo")

        username, password = user_info.split('@', 1)

        # 테스트용 계정 처리
        if username == "test" and password == "test":
            user_id = "test_user_id"
        else:
            user_id = await verify_login(username, password)

        create_session(kakaoId, user_id, username, password)
        response = create_kakao_response(
            outputs=[{"simpleText": {"text": f"Login successful for user {username}"}}]
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail="Login failed: " + str(e))

@router.post("/login/validation")
async def validate_user_info(request: Request):
    try:
        body = await request.json()
        user_info = body["value"]["resolved"]

        if '@' not in user_info:
            return {
                "status": "FAIL",
                "value": user_info,
                "data": {},
                "message": "Invalid format for userInfo. Expected 'username@password'."
            }

        username, password = user_info.split('@', 1)

        # 검증 로직
        if not username or not password:
            return {
                "status": "FAIL",
                "value": user_info,
                "data": {},
                "message": "Username or password cannot be empty."
            }

        # 테스트용 계정 처리
        if username == "test" and password == "test":
            return {
                "status": "SUCCESS",
                "value": user_info,
                "data": {},
                "message": "Validation successful."
            }

        # 실제 검증 로직
        try:
            user_id = await verify_login(username, password)
            return {
                "status": "SUCCESS",
                "value": user_info,
                "data": {},
                "message": "Validation successful."
            }
        except Exception as e:
            return {
                "status": "FAIL",
                "value": user_info,
                "data": {},
                "message": "Validation failed: Invalid username or password."
            }

    except Exception as e:
        return {
            "status": "ERROR",
            "value": "",
            "data": {},
            "message": f"Validation failed: {str(e)}"
        }

