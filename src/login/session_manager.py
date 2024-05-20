from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Dict

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 세션 저장소 (메모리 사용 예시)
user_sessions: Dict[str, dict] = {}

def create_session(kakao_id: str, user_id: str, username: str, password: str):
    expiration = datetime.utcnow() + timedelta(hours=12)
    user_sessions[kakao_id] = {"id": user_id, "username": username, "password": password, "expires": expiration}

def get_user_session(token: str = Depends(oauth2_scheme)) -> dict:
    if token not in user_sessions or user_sessions[token]['expires'] < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    return user_sessions[token]

# 주기적으로 세션을 정리하는 함수 (예시로 사용 가능)
def clear_expired_sessions():
    current_time = datetime.utcnow()
    expired_sessions = [kakao_id for kakao_id, session in user_sessions.items() if session['expires'] < current_time]
    for kakao_id in expired_sessions:
        del user_sessions[kakao_id]

